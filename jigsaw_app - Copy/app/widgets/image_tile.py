from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize

class ImageTile(QLabel):
    def __init__(self, pixmap: QPixmap, row: int, col: int, index: int):
        super().__init__()
        self.setPixmap(pixmap)
        self.setScaledContents(True)
        self.row = row
        self.col = col
        self.index = index  # original index for solved check
        self.setFixedSize(QSize(pixmap.width(), pixmap.height()))
        self.setProperty("selected", False)

    def mousePressEvent(self, e):
        self.setProperty("selected", not self.property("selected"))
        self.style().unpolish(self)
        self.style().polish(self)