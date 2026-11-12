
import os
import socket
import sys
import logging
import stat

from backends.linux import cleanup_orphans
from controller import Controller
from paths import socket_path, state_directory


logger = logging.getLogger(__name__)
MAX_COMMAND_SIZE = 1024
CLIENT_READ_TIMEOUT = 1.0


def receive_command(connection):
    
    chunks = []
    size = 0
    connection.settimeout(CLIENT_READ_TIMEOUT)

    while True:
        try:
            chunk = connection.recv(min(4096, MAX_COMMAND_SIZE + 1 - size))
        except socket.timeout:
            if not chunks:
                return None, "ERROR: Empty command"
            return None, "ERROR: Incomplete command"

        if not chunk:
            if not chunks:
                return None, "ERROR: Empty command"
            break

        chunks.append(chunk)
        size += len(chunk)
        if size > MAX_COMMAND_SIZE:
            return None, "ERROR: Command too large"

    try:
        command = b"".join(chunks).decode("utf-8").strip()
    except UnicodeDecodeError:
        return None, "ERROR: Invalid command encoding"

    if not command:
        return None, "ERROR: Empty command"
    return command, None

def another_daemon_is_alive(path):
    probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        probe.connect(str(path))
        return True

    except (ConnectionRefusedError, FileNotFoundError):
        return False

    finally:
        probe.close()


def remove_stale_socket(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        return
    if not stat.S_ISSOCK(info.st_mode) or info.st_uid != os.getuid():
        raise RuntimeError(f"Refusing to remove unexpected socket path: {path}")
    path.unlink()


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

        started, message = controller.start(minutes)

        if not started:
            return message, False

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

        return controller.status(), False

    elif action == "shutdown":
        if len(parts) != 1:
            return "ERROR: Usage: shutdown", False

        return "Daemon shutting down.", True

    return "ERROR: Unknown command", False


def start_daemon():
    socket_file = socket_path()
    log_dir = state_directory()
    logging.basicConfig(
        filename=log_dir / "daemon.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    if another_daemon_is_alive(socket_file):
        sys.exit("DozeGuard daemon is already running")

    remove_stale_socket(socket_file)

    cleanup_orphans()

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    controller = Controller(battery_floor=30)

    try:
        server.bind(str(socket_file))
        socket_file.chmod(0o600)
        server.listen()
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
                command, protocol_error = receive_command(connection)
                if protocol_error:
                    connection.sendall(protocol_error.encode())
                    continue

                try:
                    response, should_shutdown = handle_command(command, controller)
                except Exception as error:
                    logger.exception("Command failed")
                    response, should_shutdown = (
                        f"ERROR: {error}", False
                    )

                connection.sendall(response.encode())

                if should_shutdown:
                    running = False

    finally:
        try:
            controller.stop()
        except Exception:
            logger.exception("Failed to stop controller during daemon cleanup")
        finally:
            try:
                server.close()
            except OSError:
                logger.exception("Failed to close daemon socket")

            try:
                info = socket_file.lstat()
                if stat.S_ISSOCK(info.st_mode) and info.st_uid == os.getuid():
                    socket_file.unlink()
            except FileNotFoundError:
                pass
            except OSError:
                logger.exception("Failed to remove daemon socket")

            logger.info("DozeGuard daemon stopped")


if __name__ == "__main__":
    start_daemon()
