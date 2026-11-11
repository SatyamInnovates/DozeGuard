"""Linux power and battery integrations."""
import asyncio
import logging
import os

import psutil

from backends.inhibitor import Inhibitor, InhibitorError

logger = logging.getLogger(__name__)
MARKER = "--why=DozeGuard keep-awake session"


class LogindInhibitor(Inhibitor):
    """Block sleep through systemd-logind's system D-Bus API."""

    def __init__(self):
        self.fd = None

    async def _acquire(self):
        # Import lazily so battery/CLI operations can run if dbus-next is absent.
        from dbus_next.aio import MessageBus
        from dbus_next.constants import BusType

        bus = await MessageBus(
            bus_type=BusType.SYSTEM, negotiate_unix_fd=True
        ).connect()
        try:
            introspection = await bus.introspect(
                "org.freedesktop.login1", "/org/freedesktop/login1"
            )
            obj = bus.get_proxy_object(
                "org.freedesktop.login1", "/org/freedesktop/login1", introspection
            )
            manager = obj.get_interface("org.freedesktop.login1.Manager")
            return await manager.call_inhibit(
                "sleep", "DozeGuard", "DozeGuard keep-awake session", "block"
            )
        finally:
            bus.disconnect()

    def start(self):
        if self.fd is not None:
            return
        try:
            self.fd = asyncio.run(self._acquire())
        except Exception as error:
            raise InhibitorError(
                "Sleep inhibition requires an accessible systemd-logind service "
                "on the system D-Bus"
            ) from error

    def stop(self):
        if self.fd is not None:
            fd, self.fd = self.fd, None
            os.close(fd)


# Backwards-compatible name used by the controller and existing callers.
LinuxInhibitor = LogindInhibitor


def create_inhibitor(backend="logind"):
    if backend != "logind":
        raise ValueError(f"Unsupported sleep inhibition backend: {backend}")
    return LogindInhibitor()


def cleanup_orphans():
    """Retain legacy marker-based cleanup for explicitly marked processes."""
    ended = 0
    for proc in psutil.process_iter(["cmdline"]):
        try:
            cmd = proc.info["cmdline"] or []
            if MARKER in cmd:
                proc.terminate()
                ended += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            logger.debug("Could not clean marked process", exc_info=True)
    return ended


def read_battery():
    """Return (percentage, plugged-in), or (None, None) when unknown."""
    try:
        battery = psutil.sensors_battery()
    except (OSError, RuntimeError, NotImplementedError) as error:
        logger.warning("Battery status unavailable: %s", error)
        return None, None
    if battery is None:
        return None, None
    percent = battery.percent
    if percent is not None and not 0 <= percent <= 100:
        logger.warning("Ignoring invalid battery percentage: %r", percent)
        percent = None
    return percent, battery.power_plugged
