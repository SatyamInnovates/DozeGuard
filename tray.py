
import subprocess
import sys
import socket

from paths import socket_path


def main():
    try:
        from PySide6.QtCore import QTimer
        from PySide6.QtGui import QColor, QIcon, QPixmap
        from PySide6.QtWidgets import (
            QApplication,
            QMenu,
            QSystemTrayIcon,
            QMainWindow,
            QLabel,
            QPushButton,
            QVBoxLayout,
            QWidget,
        )
    except ImportError as error:
        raise SystemExit(
            "The GUI requires PySide6. Install DozeGuard with "
            "its 'tray' extra."
        ) from error

    app = QApplication(sys.argv)

    tray_available = QSystemTrayIcon.isSystemTrayAvailable()

    tray = QSystemTrayIcon() if tray_available else None


    status_label = QLabel("Checking DozeGuard status...")

    

    def run_cli(*args):
        result = subprocess.run(
            [sys.executable, "-m", "main", *args],
            capture_output=True,
            text=True,
            check=False,
        )

        message = result.stdout.strip() or result.stderr.strip()
        message = message or "Command completed."

        is_warning = (
            result.returncode != 0
            or "Battery too low" in message
        )

        if tray_available:
            icon_type = (
                QSystemTrayIcon.MessageIcon.Warning
                if is_warning
                else QSystemTrayIcon.MessageIcon.Information
            )

            tray.showMessage(
                "DozeGuard",
                message,
                icon_type,
                5000,
            )
        else:
            status_label.setText(message)

    def show_main_window():
        window = QMainWindow()
        window.setWindowTitle("DozeGuard")
        window.resize(350, 220)

        central = QWidget()
        layout = QVBoxLayout(central)

        title = QLabel("DozeGuard")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        description = QLabel(
            "Prevent your laptop from sleeping while you work."
        )

        start_button = QPushButton("Start 30 minutes")
        start_button.clicked.connect(
            lambda: run_cli("start", "30")
        )

        unlimited_button = QPushButton("Start unlimited")
        unlimited_button.clicked.connect(
            lambda: run_cli("start")
        )

        stop_button = QPushButton("Stop session")
        stop_button.clicked.connect(
            lambda: run_cli("stop")
        )

        layout.addWidget(title)
        layout.addWidget(description)
        status_label.setStyleSheet("font-size: 15px; font-weight: bold; padding: 8px;")
        layout.addWidget(status_label)
        layout.addWidget(start_button)
        layout.addWidget(unlimited_button)
        layout.addWidget(stop_button)

        window.setCentralWidget(central)
        window.show()

        return window

    if tray_available:
        menu = QMenu()

        menu.addAction("Start 30 min").triggered.connect(
            lambda: run_cli("start", "30")
        )

        menu.addAction("Start unlimited").triggered.connect(
            lambda: run_cli("start")
        )

        menu.addAction("Stop").triggered.connect(
            lambda: run_cli("stop")
        )

        menu.addSeparator()

        menu.addAction("Quit DozeGuard").triggered.connect(
            app.quit
        )

        tray.setContextMenu(menu)

    def make_icon(color):
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor(color))
        return QIcon(pixmap)


    
    def refresh():
        try:
            with socket.socket(
                socket.AF_UNIX,
                socket.SOCK_STREAM
            ) as client:
                client.settimeout(1)
                client.connect(str(socket_path()))
                client.sendall(b"status")
                client.shutdown(socket.SHUT_WR)

                reply = client.recv(1024).decode(
                    "utf-8",
                    errors="replace"
                )

        except OSError:
            reply = "DozeGuard daemon is not running."

        if "Status: Active" in reply:
            status_text = "ACTIVE\n" + reply
            status_color = "#16a34a"
            icon_color = "green"

        elif "not running" in reply:
            status_text = "UNAVAILABLE\n" + reply
            status_color = "#dc2626"
            icon_color = "gray"

        else:
            status_text = "IDLE\n" + reply
            status_color = "#d97706"
            icon_color = "orange"

        status_label.setText(status_text)
        status_label.setStyleSheet(
            f"font-size: 15px; font-weight: bold;"
            f"padding: 8px; color: {status_color};"
        )


        if tray_available:
            tray.setIcon(make_icon(icon_color))
            tray.setToolTip(f"DozeGuard\n{reply}")



    timer = QTimer()
    timer.timeout.connect(refresh)
    timer.start(1000)

    refresh()

    if tray_available:
        app.setQuitOnLastWindowClosed(False)
        tray.show()
    else:
        app.setQuitOnLastWindowClosed(True)
        window = show_main_window()
    if tray_available:
        app.setQuitOnLastWindowClosed(False)
        tray.show()
    else:
        app.setQuitOnLastWindowClosed(True)

    window = show_main_window()

    return app.exec()



if __name__ == "__main__":
    sys.exit(main())
