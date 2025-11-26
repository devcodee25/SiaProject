from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class HomeView(QWidget):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Jigsaw Studio Game")
        title.setObjectName("title")
        subtitle = QLabel("Curated futuristic artwork turned into cinematic jigsaw challenges.")
        subtitle.setObjectName("subtitle")

        btn_play = QPushButton("Start playing")
        btn_play.setFixedWidth(200)
        btn_gallery = QPushButton("Browse gallery")
        btn_gallery.setFixedWidth(200)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(btn_play)
        layout.addWidget(btn_gallery)

        btn_play.clicked.connect(self.signals.route_to_gallery.emit)
        btn_gallery.clicked.connect(self.signals.route_to_gallery.emit)