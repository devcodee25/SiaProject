import sys

from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog

try:
    from .hub_window import HubWindow
    from .login_dialog import LoginDialog
except ImportError:  # When executed as a standalone script
    from hub_window import HubWindow  # type: ignore
    from login_dialog import LoginDialog  # type: ignore


def main():
    app = QApplication(sys.argv)

    login = LoginDialog()
    if login.exec_() != QDialog.Accepted:
        return 0

    hub = HubWindow(login.username)
    hub.show()

    try:
        return app.exec_()
    except Exception as exc:
        QMessageBox.critical(None, "Unexpected error", str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())

