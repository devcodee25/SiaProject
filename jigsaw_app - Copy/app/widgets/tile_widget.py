from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, Qt


class TileWidget(QLabel):
    clicked = Signal(int)

    def __init__(self, index: int, width: int, height: int):
        super().__init__()
        self.index = index
        self.setObjectName("tileWidget")
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)
        self.setFixedSize(width, height)
        self.setProperty("selected", False)

    def mousePressEvent(self, event):
        self.clicked.emit(self.index)
        super().mousePressEvent(event)

    def set_selected(self, value: bool):
        self.setProperty("selected", value)
        self.style().unpolish(self)
        self.style().polish(self)


