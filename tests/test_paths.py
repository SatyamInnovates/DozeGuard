import os
import stat

import pytest

from paths import runtime_directory, socket_path, state_directory


def test_runtime_directory_uses_private_xdg_runtime(monkeypatch, tmp_path):
    runtime = tmp_path / "runtime"
    runtime.mkdir(mode=0o700)
    runtime.chmod(0o700)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(runtime))
    result = runtime_directory()
    assert result == runtime / "dozeguard"
    assert stat.S_IMODE(result.stat().st_mode) == 0o700
    assert result.stat().st_uid == os.getuid()


def test_runtime_directory_falls_back_for_public_xdg_dir(monkeypatch, tmp_path):
    runtime = tmp_path / "runtime"
    runtime.mkdir(mode=0o755)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(runtime))
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    result = runtime_directory()
    assert result == tmp_path / "home/.local/run/dozeguard"
    assert stat.S_IMODE(result.stat().st_mode) == 0o700


def test_state_dir_and_socket_override(monkeypatch, tmp_path):
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    runtime = tmp_path / "run"
    runtime.mkdir(mode=0o700)
    runtime.chmod(0o700)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(runtime))
    assert state_directory() == state / "dozeguard"
    assert socket_path() == runtime / "dozeguard/daemon.sock"
