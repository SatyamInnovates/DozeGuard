"""Per-user runtime and state paths for DozeGuard."""
import os
import stat
from pathlib import Path


APP_NAME = "dozeguard"


def _private_directory(path: Path) -> Path:
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid():
        raise RuntimeError(f"DozeGuard directory is not owned by this user: {path}")
    if info.st_mode & 0o077:
        path.chmod(0o700)
    return path


def state_directory() -> Path:
    base = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state")
    return _private_directory(base / APP_NAME)


def runtime_directory() -> Path:
    xdg_runtime = os.environ.get("XDG_RUNTIME_DIR")
    if xdg_runtime:
        base = Path(xdg_runtime)
        try:
            info = base.stat()
            if (stat.S_ISDIR(info.st_mode) and info.st_uid == os.getuid()
                    and not info.st_mode & 0o077):
                return _private_directory(base / APP_NAME)
        except OSError:
            pass
    return _private_directory(Path.home() / ".local/run" / APP_NAME)


def socket_path() -> Path:
    path = runtime_directory() / "daemon.sock"
    if len(os.fsencode(path)) >= 104:
        raise RuntimeError("DozeGuard runtime socket path exceeds Unix socket limits")
    return path



