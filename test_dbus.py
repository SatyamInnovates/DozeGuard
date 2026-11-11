
import asyncio

from dbus_next.aio import MessageBus
from dbus_next.constants import BusType


async def main():
    bus = await MessageBus(
        bus_type=BusType.SYSTEM,
        negotiate_unix_fd=True
    ).connect()

    print("Connected to system D-Bus!")

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

    print("Inhibitor acquired!")
    print("Returned FD:", fd)

    await asyncio.Event().wait()
    print("Connected to systemd-logind!")


asyncio.run(main())



