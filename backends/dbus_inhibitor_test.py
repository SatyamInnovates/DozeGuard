
import asyncio
import os

from dbus_next.aio import MessageBus
from dbus_next.constants import BusType


class DBusInhibitor:

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

        self.fd = asyncio.run(self._acquire())

        print(f"Sleep inhibitor acquired. FD: {self.fd}")

    def stop(self):
        if self.fd is None:
            return

        os.close(self.fd)
        self.fd = None

        print("Sleep inhibitor released.")


if __name__ == "__main__":
    inhibitor = DBusInhibitor()

    try:
        inhibitor.start()
        input("Inhibitor active. Press Enter to stop...")
    finally:
        inhibitor.stop()
