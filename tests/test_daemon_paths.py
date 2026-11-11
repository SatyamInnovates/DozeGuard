import socket
import stat

import pytest

from daemon import another_daemon_is_alive, remove_stale_socket


def test_remove_stale_owned_socket(tmp_path):
    path = tmp_path / "daemon.sock"
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(str(path))
    server.close()
    remove_stale_socket(path)
    assert not path.exists()


def test_remove_stale_socket_refuses_regular_file(tmp_path):
    path = tmp_path / "daemon.sock"
    path.write_text("keep")
    with pytest.raises(RuntimeError, match="Refusing"):
        remove_stale_socket(path)
    assert path.read_text() == "keep"


def test_live_socket_is_detected(tmp_path):
    path = tmp_path / "daemon.sock"
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(str(path))
    server.listen()
    try:
        assert another_daemon_is_alive(path)
    finally:
        server.close()
