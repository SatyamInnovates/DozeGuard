import socket
import os

SOCKET_PATH = "/tmp/dozeguard.sock"



def handle_command(command):
    parts = command.split()

    if not parts:
        return "ERROR: Empty command",False

    action = parts[0]

    if action == "start":
        if len(parts) >2:
            return "ERROR: Usage: Start[minutes]",False

        if len(parts) == 2:
            try:
                minutes = int(parts[1])
                if minutes <= 0:
                    return "ERROR: Minutes must be positive", False
            except ValueError:
                return "ERROR: Minuts must be a number",False
            return f"Recognized: start for {minutes} minutes",False

        return "Recognized: unlimited start", False
    elif action == "stop":
        if len(parts) != 1:
            return "ERROR: Usage: stop", False
        return "Recognized: stop", False

    elif action == "status":
        if len(parts) != 1:
            return "ERROR: Usage: status", False
        return "Recognized: status", False

    elif action == "shutdown":
        if len(parts) != 1:
            return "ERROR: Usage: shutdown", False
        return "Daemon shutting down", True

    return "ERROR: Unknown command", False
 


def start_daemon():
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)

        server.bind(SOCKET_PATH)
        server.listen()

        print("DozeGuard daemon is running...")

        running = True

        while running:
            connection, _ = server.accept()

            with connection:
                data = connection.recv(1024)

                if not data:
                    continue

                command = data.decode().strip()
                print("Received:", command)

                response, should_shutdown = handle_command(command)
                connection.sendall(response.encode())

                if should_shutdown:
                    running = False

    finally:
        server.close()

        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)

        print("DozeGuard daemon stopped.")


if __name__ == "__main__":
    start_daemon()
