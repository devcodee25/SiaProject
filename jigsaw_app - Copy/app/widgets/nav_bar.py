from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class NavBar(QFrame):
    def __init__(self, title: str, on_home, on_back):
        super().__init__()
        self.setObjectName("toolbar")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        btn_back = QPushButton("Back")
        btn_home = QPushButton("Home")
        self.lbl_title = QLabel(title)
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setStyleSheet("font-weight: 600;")
        layout.addWidget(btn_back)
        layout.addWidget(self.lbl_title, 1)
        layout.addWidget(btn_home)

        btn_home.clicked.connect(on_home)
        btn_back.clicked.connect(on_back)

    def set_title(self, title: str):
        self.lbl_title.setText(title)