import socket
import subprocess
import sys
from pathlib import Path
from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor, QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon



SOCKET_PATH = "/tmp/dozeguard.sock"
MAIN = Path(__file__).parent / "main.py"


def ask_daemon(command):
    client = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    client.settimeout(2)
    try:
        client.connect(SOCKET_PATH)
        client.sendall(command.encode())
        return client.recv(1024).decode()
    except (FileNotFoundError, ConnectionRefusedError, socket.timeout):
        return None
    finally:
        client.close()


def run_cli(*args):
    result = subprocess.run(
        [sys.executable,str(MAIN),*args],
        cwd=MAIN.parent,
        capture_output=True,
        text=True
    )


    message = result.stdout.strip() or result.stderr.strip()

    if "Battery too low" in message:
        icon = QSystemTrayIcon.MessageIcon.Warning
    else:
        icon = QSystemTrayIcon.MessageIcon.Information


    tray.showMessage("DozeGuard",message or "Something went wrong",icon,5000)

def make_icon(color):
    pix = QPixmap(64, 64)
    pix.fill(QColor(color))
    return QIcon(pix)


app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

tray = QSystemTrayIcon()
menu = QMenu()
menu.addAction("Start 30 min").triggered.connect(lambda: run_cli("start", "30"))
menu.addAction("Start unlimited").triggered.connect(lambda: run_cli("start"))
menu.addAction("Stop").triggered.connect(lambda: run_cli("stop"))
menu.addSeparator()
menu.addAction("Quit tray").triggered.connect(app.quit)



tray.setContextMenu(menu)

def refresh():
    reply = ask_daemon("status")

    if reply is None:
        tray.setIcon(make_icon("gray"))
        tray.setToolTip("DozeGuard: daemon not running")

    elif "Status: Active" in reply:
        tray.setIcon(make_icon("green"))
        tray.setToolTip(f"DozeGuard\n{reply}")
    else:
        tray.setIcon(make_icon("orange"))
        tray.setToolTip("DozeGuard: idle")





timer = QTimer()
timer.timeout.connect(refresh)
timer.start(1000)         
refresh()                 

tray.show()
sys.exit(app.exec())



