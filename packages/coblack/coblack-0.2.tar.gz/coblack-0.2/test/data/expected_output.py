import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMenu,
    QSystemTrayIcon,
)

from .icon import icon_path
from .notebook_server import NotebookServer
from .control_window import ControlWindow


def make_menu(app, server, control_window):
    def quit():
        server.stop()  # Prevent garbage collection, to prevent closing
        app.tray_icon: QSystemTrayIcon
        app.tray_icon.hide()  # Prevent lingering of a ghost tray icon (that disappears
        #                     # on hover) after process has already exited.
        app.quit()

    menu = QMenu()
    menu.addAction("Settings").triggered.connect(control_window.show_and_activate)
    menu.addAction("Restart server").triggered.connect(server.restart)  # This is a
    #                                       # comment that is already multiline but
    #                                       # obviously not good.
    menu.addAction("Exit").triggered.connect(quit)
    return menu


def make_tray_icon(app, menu, control_window):
    tray_icon = QSystemTrayIcon(QIcon(str(icon_path)), parent=app)  # And this is a
    #                                       # comment that is multiline _and_ with extra
    #                                       # `#`. But no good yet.

    # And here's a newline before. Ergo: new comment, don't join pls.
    tray_icon.setToolTip("Jupytray")
    tray_icon.setContextMenu(menu)

    def on_tray_icon_activated(reason: QSystemTrayIcon.ActivationReason):
        if reason != QSystemTrayIcon.Context:
            if control_window.isHidden():
                # Please make this simple comment that does not follow code on the same
                # line multiline, thanks you.
                control_window.show_and_activate()
            else:
                control_window.hide()

    tray_icon.activated.connect(on_tray_icon_activated)
    tray_icon.show()
    app.tray_icon = tray_icon  # Save ref to tray icon so we can hide it on app exit.
