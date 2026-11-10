import os
import socket
import sys
from backends.linux import cleanup_orphans
from controller import Controller
import logging
from pathlib import Path



LOG_DIR = Path.home() / ".local" / "state" / "dozeguard"
LOG_DIR.mkdir(parents=True, exist_ok=True)


logging.basicConfig(
    filename=LOG_DIR / "daemon.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",

)



SOCKET_PATH = "/tmp/dozeguard.sock"


def another_daemon_is_alive(path):
    probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        probe.connect(path)
        return True               
    except ConnectionRefusedError:
        return False              
    except FileNotFoundError:
        return False              
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

        started,message = controller.start(minutes)
        if not started:
            return message,False
        duration = f"{minutes} minutes" if minutes else "unlimited"
        return f"DozeGuard started : {duration}", False


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

        # Wake up
        server.settimeout(1)

        print("DozeGuard daemon is running...")

        running = True

        while running:
            try:
                connection, _ = server.accept()
            except socket.timeout:
                controller.tick()
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