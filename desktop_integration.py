"""User-level desktop integration helpers for the optional tray frontend."""

from __future__ import annotations

import fcntl
import os
import sys
from pathlib import Path


AUTOSTART_NAME = "dozeguard-tray.desktop"
MANAGED_MARKER = "X-DozeGuard-Managed=true"


def _desktop_quote(value: str) -> str:
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("`", "\\`")
        .replace("$", "\\$")
    )
    return f'"{escaped}"'


def user_autostart_path() -> Path:
    config_home = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return config_home / "autostart" / AUTOSTART_NAME


def _user_override_contents(hidden: bool) -> str:
    return (
        "[Desktop Entry]\n"
        "Type=Application\n"
        "Name=DozeGuard\n"
        "Comment=Keep this session awake\n"
        f"Exec={_desktop_quote(sys.executable)} -m tray --background\n"
        f"TryExec={_desktop_quote(sys.executable)}\n"
        "Terminal=false\n"
        "X-GNOME-Autostart-enabled=true\n"
        f"{MANAGED_MARKER}\n"
        f"Hidden={'true' if hidden else 'false'}\n"
    )


def set_autostart_enabled(enabled: bool) -> Path:
    """Write a managed XDG user override to enable or disable autostart."""
    path = user_autostart_path()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if path.exists() and MANAGED_MARKER not in path.read_text(encoding="utf-8"):
        raise FileExistsError(
            f"Refusing to replace an unmanaged autostart entry: {path}"
        )
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(_user_override_contents(hidden=not enabled))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return path


class TrayInstanceLock:
    """Advisory per-user lock that prevents duplicate tray processes."""

    def __init__(self, file_descriptor: int):
        self._fd = file_descriptor

    @classmethod
    def acquire(cls, path: Path) -> TrayInstanceLock | None:
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
        os.fchmod(fd, 0o600)
        os.set_inheritable(fd, False)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            os.close(fd)
            return None
        except BaseException:
            os.close(fd)
            raise
        return cls(fd)

    def close(self) -> None:
        if self._fd is not None:
            fcntl.flock(self._fd, fcntl.LOCK_UN)
            os.close(self._fd)
            self._fd = None

    def __enter__(self) -> TrayInstanceLock:
        return self

    def __exit__(self, *_exc) -> None:
        self.close()
