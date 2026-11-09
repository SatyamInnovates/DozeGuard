import os
import socket
import sys

from backends.linux import cleanup_orphans
from controller import Controller

SOCKET_PATH = "/tmp/dozeguard.sock"


def another_daemon_is_alive(path):
    probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        probe.connect(path)
        return True               # connected: a live daemon is there
    except ConnectionRefusedError:
        return False              # stale file, nobody listening
    except FileNotFoundError:
        return False              # no file at all
    finally:
        probe.close()


def handle_command(command, controller):
    parts = command.split()

    if not parts:
        return "ERROR: Empty command", False

    action = parts[0]

    if action == "start":
        if len(parts) > 2:
            return "ERROR: Usage: start [minutes]", False

        minutes = None

        if len(parts) == 2:
            try:
                minutes = int(parts[1])
                if minutes <= 0:
                    return "ERROR: Minutes must be positive", False
            except ValueError:
                return "ERROR: Minutes must be a number", False

        started = controller.start(minutes)

        if not started:
            return "A session is already active.", False

        duration = f"{minutes} minutes" if minutes else "unlimited"
        return f"DozeGuard started: {duration}", False

    elif action == "stop":
        if len(parts) != 1:
            return "ERROR: Usage: stop", False

        controller.stop()
        return "DozeGuard stopped.", False

    elif action == "status":
        if len(parts) != 1:
            return "ERROR: Usage: status", False

        if controller.is_active():
            return "Status: Active", False

        return "Status: Inactive", False

    elif action == "shutdown":
        if len(parts) != 1:
            return "ERROR: Usage: shutdown", False

        return "Daemon shutting down.", True

    return "ERROR: Unknown command", False


def start_daemon():
    if another_daemon_is_alive(SOCKET_PATH):
        sys.exit("DozeGuard daemon is already running")


    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    cleanup_orphans()

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    controller = Controller()

    try:
        server.bind(SOCKET_PATH)
        server.listen()

        # Wake up periodically to check the session timer.
        server.settimeout(1)

        print("DozeGuard daemon is running...")

        running = True

        while running:
            try:
                connection, _ = server.accept()
            except socket.timeout:
                controller.is_active()
                continue

            with connection:
                data = connection.recv(1024)

                if not data:
                    continue

                command = data.decode().strip()
                print("Received:", command)

                response, should_shutdown = handle_command(
                    command, controller
                )

                connection.sendall(response.encode())

                if should_shutdown:
                    running = False

    finally:
        controller.stop()
        server.close()

        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)

        print("DozeGuard daemon stopped.")


if __name__ == "__main__":
    start_daemon()