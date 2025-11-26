import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


@dataclass
class SuiteApp:
    name: str
    description: str
    entry_point: str
    process: Optional[subprocess.Popen] = None


class HubWindow(QMainWindow):
    """Second-stage UI where the user selects which experience to launch."""

    def __init__(self, username: str, parent=None):
        super().__init__(parent)
        self.username = username
        self.apps = self._build_app_catalog()

        self.setWindowTitle("Media and Entertainment")
        self.resize(720, 420)
        self._apply_palette()
        self._build_ui()

    def _build_app_catalog(self):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return [
            SuiteApp(
                name="🎬 Movies Hub",
                description="Browse our featured movie and TV show collections.",
                entry_point=os.path.join(root, "MoviesHub-main - Copy", "moviehub.py"),
            ),
            SuiteApp(
                name="🎧 Music Media Player",
                description="Full media player with playlists and theming.",
                entry_point=os.path.join(root, "siamusic - Copy", "main.py"),
            ),
            SuiteApp(
                name="🧩 Jigsaw Game",
                description="Solve puzzles with dynamic gallery selection.",
                entry_point=os.path.join(root, "jigsaw_app - Copy", "main.py"),
            ),
        ]

    def _build_ui(self):
        container = QWidget()
        container.setObjectName("hubRoot")
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        hero = QFrame()
        hero.setObjectName("heroCard")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(24, 20, 24, 20)
        hero_layout.setSpacing(4)

        greeting = QLabel(f"Hi {self.username}, welcome to EntertainHub✨")
        greeting.setObjectName("heroTitle")
        hero_layout.addWidget(greeting)

        hint = QLabel("Choose an experience to open in a separate window.")
        hint.setObjectName("heroSubtitle")
        hero_layout.addWidget(hint)

        layout.addWidget(hero)

        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(18)

        for index, suite_app in enumerate(self.apps):
            card = self._build_app_card(suite_app)
            row, col = divmod(index, 2)
            grid.addWidget(card, row, col)

        layout.addLayout(grid)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _build_app_card(self, suite_app: SuiteApp):
        frame = QFrame()
        frame.setObjectName("appCard")

        vbox = QVBoxLayout()
        title = QLabel(suite_app.name)
        title.setObjectName("cardTitle")
        title.setWordWrap(False)
        vbox.addWidget(title)

        desc = QLabel(suite_app.description)
        desc.setWordWrap(True)
        desc.setObjectName("cardSubtitle")
        vbox.addWidget(desc)

        vbox.addStretch()

        launch_btn = QPushButton("Open app")
        launch_btn.setProperty("entry_point", suite_app.entry_point)
        launch_btn.setObjectName("cardButton")
        launch_btn.clicked.connect(lambda _, app=suite_app: self.launch_app(app))
        vbox.addWidget(launch_btn)

        frame.setLayout(vbox)
        return frame

    def launch_app(self, suite_app: SuiteApp):
        entry = suite_app.entry_point
        if not os.path.exists(entry):
            QMessageBox.warning(self, "Missing file", f"Cannot find {entry}")
            return

        try:
            cmd = [sys.executable, entry]
            if "siamusic" in entry.lower():
                cmd.append(f"--username={self.username}")
            env = os.environ.copy()
            env["SIA_USERNAME"] = self.username
            suite_app.process = subprocess.Popen(cmd, env=env)
        except OSError as exc:
            QMessageBox.critical(self, "Launch failed", str(exc))

    def closeEvent(self, event):
        """Keep hub closing simple; leave launched apps running."""
        for app in self.apps:
            if app.process and app.process.poll() is None:
                continue
        super().closeEvent(event)

    def _apply_palette(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background: #fdf7ff;
                font-family: 'Segoe UI', 'Poppins', Arial;
            }
            QWidget#hubRoot {
                background: transparent;
            }
            QFrame#heroCard {
                border-radius: 18px;
                border: 1px solid #f1d8ff;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #ffe9ff, stop:1 #e3f4ff);
            }
            QLabel#heroTitle {
                font-size: 20px;
                font-weight: 700;
                color: #34235c;
            }
            QLabel#heroSubtitle {
                color: #6b5b87;
                font-size: 14px;
            }
            QFrame#appCard {
                border-radius: 16px;
                border: 1px solid #f3dcff;
                background: #ffffff;
                padding: 18px;
                min-width: 300px;
                max-width: 300px;
            }
            QLabel#cardTitle {
                font-size: 18px;
                font-weight: 600;
                color: #2e1d4f;
            }
            QLabel#cardSubtitle {
                color: #7a6a92;
            }
            QPushButton#cardButton {
                margin-top: 12px;
                padding: 10px 0;
                border-radius: 10px;
                border: none;
                font-weight: 600;
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #ffb1d1, stop:1 #b48dff);
            }
            QPushButton#cardButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #ffc1da, stop:1 #c49dff);
            }
            """
        )

