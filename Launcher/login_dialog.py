import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
)

# Re-use the existing authentication logic from the siamusic project.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SIAMUSIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Music"))

if SIAMUSIC_DIR not in sys.path:
    sys.path.append(SIAMUSIC_DIR)

from database import UserDatabase  # type: ignore  # imported via sys.path hack


class LoginDialog(QDialog):
    """Simple login dialog that authenticates against the shared user database."""

    def __init__(self, parent=None):
        super().__init__(parent)
        db_path = os.path.join(SIAMUSIC_DIR, "users.db")
        self.db = UserDatabase(db_path=db_path)
        self.username = ""

        self._ensure_default_user()
        self._build_ui()

    def _ensure_default_user(self):
        """Create a fallback demo account so first-time users can log in."""
        default_user = "admin"
        default_password = "admin123"
        if not self.db.user_exists(default_user):
            self.db.create_user(default_user, default_password)

    def _build_ui(self):
        self.setWindowTitle("SIA Suite Login")
        self.setFixedSize(360, 260)

        wrapper = QVBoxLayout(self)
        wrapper.setContentsMargins(24, 24, 24, 24)
        wrapper.addStretch()

        card = QFrame()
        card.setObjectName("loginCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)
        card_layout.setContentsMargins(32, 32, 32, 32)

        title = QLabel("Welcome to EntertainHub👋")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("loginTitle")
        card_layout.addWidget(title)


        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        card_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password_input)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setObjectName("statusLabel")
        card_layout.addWidget(self.status_label)

        login_btn = QPushButton("Login")
        login_btn.setObjectName("primaryButton")
        login_btn.clicked.connect(self._on_login_clicked)
        card_layout.addWidget(login_btn)

        self.password_input.returnPressed.connect(self._on_login_clicked)

        wrapper.addWidget(card, alignment=Qt.AlignCenter)
        wrapper.addStretch()

        self.setStyleSheet(
            """
        QDialog {
        min-width: 550px; 
        min-height: 550px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                     stop:0 #fef1ff, stop:1 #e2f4ff);
    }
    QFrame#loginCard {
        background: #ffffff;
        border-radius: 20px;
        border: 1px solid #f1d8ff;
        box-shadow: 0px 15px 30px rgba(165, 125, 255, 0.15);
        min-width: 450px; 
        min-height: 450px;
    }
    QLabel#loginTitle {
        font-size: 22px;
        font-weight: 700;
        color: #2b1f4b;
    }
    QLabel#loginSubtitle {
        color: #7a6b9d;
    }
    QLineEdit {
        padding: 10px 14px;
        border: 2px solid #f1e5ff;
        border-radius: 10px;
        font-size: 14px;
        background: #fcfbff;
    }
    QLineEdit:focus {
        border-color: #a074ff;
        background: #ffffff;
    }
    QPushButton#primaryButton {
        padding: 12px;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        color: white;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                     stop:0 #ff9acd, stop:1 #a372ff);
    }
    QPushButton#primaryButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                     stop:0 #ffaad6, stop:1 #b283ff);
    }
    QLabel#statusLabel {
        min-height: 20px;
        color: #e05a6e;
    }
            """
        )

    def _on_login_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            self._set_error("Please enter username and password.")
            return

        if self.db.authenticate_user(username, password):
            self.username = username
            self.accept()
        else:
            self._set_error("Invalid credentials. Try again.")

    def _set_error(self, message: str):
        self.status_label.setText(message)
        self.password_input.clear()
        self.password_input.setFocus()

