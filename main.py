import argparse
import socket
import subprocess
import sys
import time
from pathlib import Path
import logging



SOCKET_PATH = "/tmp/dozeguard.sock"
BASE_DIR = Path(__file__).resolve().parent
DAEMON_PATH = BASE_DIR / "daemon.py"


def create_parser():
    parser = argparse.ArgumentParser(
        prog="DozeGuard",
        description="A Linux utility to keep your laptop awake."
    )

    parser.add_argument(
        "command",
        choices=["start", "stop", "status"],
        help="Command to execute"
    )

    parser.add_argument(
        "minutes",
        nargs="?",
        type=int,
        help="Duration in minutes (omit for unlimited)"
    )

    return parser




def send_command(command):
    client = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) 
    client.settimeout(2)

    try:
        client.connect(SOCKET_PATH)
        client.sendall(command.encode())
        response = client.recv(1024)
        return response.decode()
    finally:
        client.close()



def start_daemon():
    subprocess.Popen(
        [sys.executable, str(DAEMON_PATH)],
        cwd=str(BASE_DIR),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )


def send_command_with_autostart(command):
    try:
        return send_command(command)

    except OSError:
        start_daemon()

    deadline = time.monotonic() + 5

    while time.monotonic() < deadline:
        try:
            return send_command(command)
        except OSError:
            time.sleep(0.1)

    raise RuntimeError(
        "Could not connect to DozeGuard daemon. Check daemon errors."
    )



def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command != "start" and args.minutes is not None:
        parser.error("minutes can be suplied with 'start'")

    if args.minutes is not None and args.minutes <= 0:
        parser.error("minutes must be positive")

    command = args.command

    if args.command == "start" and args.minutes is not None:
        command = f"start {args.minutes}"

    try:
        print(send_command_with_autostart(command))
    except (OSError, RuntimeError) as error:
        print(f"DozeGuard error: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()




# done
