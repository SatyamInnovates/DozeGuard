"""Optional Qt system tray frontend for DozeGuard."""
import subprocess
import sys

from paths import socket_path


def main():
    try:
        from PySide6.QtCore import QTimer
        from PySide6.QtGui import QColor, QIcon, QPixmap
        from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
    except ImportError as error:
        raise SystemExit(
            "The optional tray requires PySide6. Install DozeGuard with its "
            "'tray' extra or distribution tray package."
        ) from error

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    if not QSystemTrayIcon.isSystemTrayAvailable():
        raise SystemExit("No system tray is available in this desktop session")

    tray = QSystemTrayIcon()
    menu = QMenu()

    def run_cli(*args):
        result = subprocess.run(
            [sys.executable, "-m", "main", *args],
            capture_output=True, text=True, check=False
        )
        message = result.stdout.strip() or result.stderr.strip()
        icon = (QSystemTrayIcon.MessageIcon.Warning
                if result.returncode or "Battery too low" in message
                else QSystemTrayIcon.MessageIcon.Information)
        tray.showMessage("DozeGuard", message or "Command failed", icon, 5000)

    menu.addAction("Start 30 min").triggered.connect(lambda: run_cli("start", "30"))
    menu.addAction("Start unlimited").triggered.connect(lambda: run_cli("start"))
    menu.addAction("Stop").triggered.connect(lambda: run_cli("stop"))
    menu.addSeparator()
    menu.addAction("Quit tray").triggered.connect(app.quit)
    tray.setContextMenu(menu)

    def icon(color):
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor(color))
        return QIcon(pixmap)

    def refresh():
        try:
            import socket
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
                client.settimeout(1)
                client.connect(str(socket_path()))
                client.sendall(b"status")
                reply = client.recv(1024).decode("utf-8", errors="replace")
        except OSError:
            reply = None
        if reply is None:
            tray.setIcon(icon("gray"))
            tray.setToolTip("DozeGuard: daemon not running")
        elif "Status: Active" in reply:
            tray.setIcon(icon("green"))
            tray.setToolTip(f"DozeGuard\n{reply}")
        else:
            tray.setIcon(icon("orange"))
            tray.setToolTip(f"DozeGuard\n{reply}")

    timer = QTimer()
    timer.timeout.connect(refresh)
    timer.start(2000)
    refresh()
    tray.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
