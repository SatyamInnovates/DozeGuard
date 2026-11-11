import asyncio
import os
import psutil
from dbus_next.aio import MessageBus
from dbus_next.constants import BusType



MARKER = "--why=DozeGuard keep-awake session"


class LinuxInhibitor:
    def __init__(self):
        self.fd = None

    async def _acquire(self):
        bus = await MessageBus(
            bus_type=BusType.SYSTEM,
            negotiate_unix_fd=True
        ).connect()

        try:
            introspection = await bus.introspect(
                "org.freedesktop.login1",
                "/org/freedesktop/login1"
            )

            obj = bus.get_proxy_object(
                "org.freedesktop.login1",
                "/org/freedesktop/login1",
                introspection
            )

            manager = obj.get_interface(
                "org.freedesktop.login1.Manager"
            )

            fd = await manager.call_inhibit(
                "sleep",
                "DozeGuard",
                "DozeGuard keep-awake session",
                "block"
            )

            return fd

        finally:
            bus.disconnect()

    def start(self):
        if self.fd is not None:
            return

        fd = asyncio.run(self._acquire())
        self.fd = fd

    def stop(self):
        if self.fd is None:
            return

        os.close(self.fd)
        self.fd = None


def cleanup_orphans():
    ended = 0

    for proc in psutil.process_iter(["cmdline"]):
        cmd = proc.info["cmdline"] or []

        if MARKER in cmd:
            try:
                proc.terminate()
                ended += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    return ended


def read_battery():
    battery = psutil.sensors_battery()

    if battery is None:
        return None, True

    return battery.percent, battery.power_plugged
