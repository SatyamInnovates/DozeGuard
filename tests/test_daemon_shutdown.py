import socket
import threading
import time

import pytest

import daemon
import main


class StubController:
    def __init__(self, fail_on_stop=False):
        self.stop_calls = 0
        self.fail_on_stop = fail_on_stop

    def stop(self):
        self.stop_calls += 1
        if self.fail_on_stop:
            raise OSError("simulated inhibitor release error")

    def tick(self):
        pass


@pytest.mark.parametrize("fail_on_stop", [False, True])
def test_shutdown_replies_stops_controller_and_removes_socket(
    monkeypatch, tmp_path, fail_on_stop
):
    runtime = tmp_path / "runtime"
    runtime.mkdir(mode=0o700)
    socket_file = runtime / "daemon.sock"
    state_dir = tmp_path / "state"
    state_dir.mkdir(mode=0o700)
    controller = StubController(fail_on_stop=fail_on_stop)

    monkeypatch.setattr(daemon, "socket_path", lambda: socket_file)
    monkeypatch.setattr(daemon, "state_directory", lambda: state_dir)
    monkeypatch.setattr(daemon.logging, "basicConfig", lambda **kwargs: None)
    monkeypatch.setattr(daemon, "cleanup_orphans", lambda: 0)
    monkeypatch.setattr(daemon, "Controller", lambda battery_floor: controller)

    thread = threading.Thread(target=daemon.start_daemon, daemon=True)
    thread.start()
    deadline = time.monotonic() + 2
    while not socket_file.exists() and thread.is_alive() and time.monotonic() < deadline:
        threading.Event().wait(0.01)

    assert socket_file.exists()
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.settimeout(2)
        client.connect(str(socket_file))
        client.sendall(b"shutdown")
        response = client.recv(1024).decode()

    thread.join(timeout=2)
    assert response == "Daemon shutting down."
    assert not thread.is_alive()
    assert controller.stop_calls == 1
    assert not socket_file.exists()


def test_shutdown_command_is_available_in_cli():
    args = main.create_parser().parse_args(["shutdown"])
    assert args.command == "shutdown"


def test_shutdown_does_not_start_a_daemon(monkeypatch):
    starts = []

    def missing_daemon(command):
        raise FileNotFoundError(command)

    monkeypatch.setattr(main, "send_command", missing_daemon)
    monkeypatch.setattr(main, "start_daemon", lambda: starts.append(True))

    with pytest.raises(FileNotFoundError):
        main.send_command_with_autostart("shutdown")

    assert starts == []


def test_shutdown_command_rejects_arguments():
    response, should_shutdown = daemon.handle_command(
        "shutdown extra", StubController()
    )
    assert response == "ERROR: Usage: shutdown"
    assert should_shutdown is False
