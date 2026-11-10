import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QPixmap, QColor

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)    # no windows exist, so don't exit

pix = QPixmap(64, 64)
pix.fill(QColor("gray"))
tray = QSystemTrayIcon(QIcon(pix))
tray.setToolTip("DozeGuard")

menu = QMenu()
quit_action = menu.addAction("Quit")
quit_action.triggered.connect(app.quit)

tray.setContextMenu(menu)
tray.show()

sys.exit(app.exec())