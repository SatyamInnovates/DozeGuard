"""Optional PySide6 desktop frontend for DozeGuard."""

from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
from pathlib import Path
from desktop_integration import TrayInstanceLock, set_autostart_enabled
from paths import runtime_directory, socket_path


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="dozeguard-tray")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--background",
        action="store_true",
        help="start the tray in the background without opening its window",
    )
    mode.add_argument(
        "--enable-autostart",
        action="store_true",
        help="enable the system-wide login autostart entry",
    )
    mode.add_argument(
        "--disable-autostart",
        action="store_true",
        help="disable DozeGuard login autostart for this user",
    )
    return parser.parse_args(argv)


def query_status() -> str:
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.settimeout(1)
            client.connect(str(socket_path()))
            client.sendall(b"status")
            client.shutdown(socket.SHUT_WR)
            return client.recv(1024).decode("utf-8", errors="replace")
    except OSError:
        return "DozeGuard daemon is not running."


def should_run_background(tray_available: bool) -> bool:
    """A login launch should stay alive only when a tray host is available."""
    return tray_available


def should_show_window(background: bool) -> bool:
    return not background


def user_tray_venv_python() -> Path:
    data_home = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share")
    return data_home / "dozeguard/tray-venv/bin/python"


def _delegate_to_user_tray_venv(argv: list[str] | None) -> None:
    try:
        import PySide6  # noqa: F401
        return
    except (ImportError, OSError):
        pass

    venv_python = user_tray_venv_python()
    if not venv_python.is_file() or venv_python.resolve() == Path(sys.executable).resolve():
        return
    try:
        probe = subprocess.run(
            [str(venv_python), "-c", "from PySide6 import QtWidgets"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError:
        return
    if probe.returncode == 0:
        forwarded = argv if argv is not None else sys.argv[1:]
        try:
            os.execv(str(venv_python), [str(venv_python), "-m", "tray", *forwarded])
        except OSError:
            return


def _run_command(args: tuple[str, ...]) -> tuple[str, bool]:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "main", *args],
            capture_output=True,
            text=True,
            check=False,
        )
        message = result.stdout.strip() or result.stderr.strip() or "Command completed."
        return message, result.returncode != 0 or "Battery too low" in message
    except OSError as error:
        return f"Unable to run DozeGuard command: {error}", True


def main(argv: list[str] | None = None) -> int:
    args = parse_arguments(argv)
    if args.enable_autostart or args.disable_autostart:
        try:
            path = set_autostart_enabled(args.enable_autostart)
        except (OSError, FileExistsError) as error:
            print(f"dozeguard-tray: {error}", file=sys.stderr)
            return 1
        state = "enabled" if args.enable_autostart else "disabled"
        print(f"DozeGuard autostart {state} for this user ({path}).")
        return 0

    _delegate_to_user_tray_venv(argv)

    try:
        lock = TrayInstanceLock.acquire(runtime_directory() / "tray.lock")
    except (OSError, RuntimeError) as error:
        print(f"dozeguard-tray: cannot create the per-user tray lock: {error}", file=sys.stderr)
        return 1
    if lock is None:
        if args.background:
            print("DozeGuard tray is already running.")
            return 0
        return _run_qt(False, argv, allow_tray=False)

    try:
        return _run_qt(args.background, argv)
    finally:
        lock.close()


def _run_qt(
    background: bool, argv: list[str] | None, *, allow_tray: bool = True
) -> int:
    try:
        from PySide6.QtCore import QTimer
        from PySide6.QtGui import QColor, QIcon, QPixmap
        from PySide6.QtWidgets import (
            QApplication,
            QLabel,
            QMainWindow,
            QMenu,
            QPushButton,
            QSystemTrayIcon,
            QVBoxLayout,
            QWidget,
        )
    except (ImportError, OSError) as error:
        print(
            "dozeguard-tray: the optional GUI requires PySide6. Install DozeGuard "
            "with its [tray] extra or the distribution's tray package.",
            file=sys.stderr,
        )
        return 0 if background else 1

    app = QApplication([sys.argv[0]])
    app.setApplicationName("DozeGuard")
    tray_available = allow_tray and QSystemTrayIcon.isSystemTrayAvailable()

    if background and not should_run_background(tray_available):
        print("DozeGuard tray not started: this desktop has no system tray host.")
        return 0

    tray = QSystemTrayIcon() if tray_available else None
    status_label = QLabel("Checking DozeGuard status…")
    window = QMainWindow()
    window.setWindowTitle("DozeGuard")
    window.resize(360, 250)
    central = QWidget()
    layout = QVBoxLayout(central)
    title = QLabel("DozeGuard")
    title.setStyleSheet("font-size: 22px; font-weight: bold;")
    layout.addWidget(title)
    layout.addWidget(QLabel("Prevent your laptop from sleeping while you work."))
    status_label.setStyleSheet("font-size: 15px; font-weight: bold; padding: 8px;")
    layout.addWidget(status_label)

    def notify(message: str, warning: bool) -> None:
        if tray is not None:
            kind = (
                QSystemTrayIcon.MessageIcon.Warning
                if warning
                else QSystemTrayIcon.MessageIcon.Information
            )
            tray.showMessage("DozeGuard", message, kind, 5000)
        else:
            status_label.setText(message)

    def run_cli(*command: str) -> None:
        message, warning = _run_command(tuple(command))
        notify(message, warning)
        refresh()

    for label, command in (
        ("Start 30 min", ("start", "30")),
        ("Start unlimited", ("start",)),
        ("Stop", ("stop",)),
    ):
        button = QPushButton(label)
        button.clicked.connect(lambda _checked=False, c=command: run_cli(*c))
        layout.addWidget(button)
    window.setCentralWidget(central)

    def make_icon(color: str) -> QIcon:
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor(color))
        return QIcon(pixmap)

    def refresh() -> None:
        reply = query_status()
        if "Status: Active" in reply:
            title_text, status_color, icon_color = "ACTIVE", "#16a34a", "green"
        elif "not running" in reply.lower():
            title_text, status_color, icon_color = "UNAVAILABLE", "#dc2626", "gray"
        else:
            title_text, status_color, icon_color = "IDLE", "#d97706", "orange"
        status_label.setText(f"{title_text}\n{reply}")
        status_label.setStyleSheet(
            f"font-size: 15px; font-weight: bold; padding: 8px; color: {status_color};"
        )
        if tray is not None:
            tray.setIcon(make_icon(icon_color))
            tray.setToolTip(f"DozeGuard\n{reply}")

    if tray is not None:
        menu = QMenu()
        menu.addAction("Open DozeGuard").triggered.connect(window.show)
        menu.addSeparator()
        menu.addAction("Start 30 min").triggered.connect(
            lambda: run_cli("start", "30")
        )
        menu.addAction("Start unlimited").triggered.connect(
            lambda: run_cli("start")
        )
        menu.addAction("Stop").triggered.connect(lambda: run_cli("stop"))
        menu.addSeparator()
        menu.addAction("Quit DozeGuard").triggered.connect(app.quit)
        tray.setContextMenu(menu)
        tray.activated.connect(
            lambda reason: window.show()
            if reason == QSystemTrayIcon.ActivationReason.Trigger
            else None
        )
        tray.show()
        app.setQuitOnLastWindowClosed(False)
    else:
        app.setQuitOnLastWindowClosed(True)

    timer = QTimer()
    timer.timeout.connect(refresh)
    timer.start(1000)
    refresh()
    if should_show_window(background):
        window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
