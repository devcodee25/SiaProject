from PySide6.QtWidgets import QMainWindow, QStackedWidget
from PySide6.QtCore import QSize
from app.signals import AppSignals
from app.theme import apply_theme
from views.home_view import HomeView
from views.gallery_view import GalleryView
from views.puzzle_view import PuzzleView

class JigsawApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jigsaw Studio Game")
        self.resize(1000, 700)
        apply_theme()

        self.signals = AppSignals()
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_view = HomeView(self.signals)
        self.gallery_view = GalleryView(self.signals)
        self.puzzle_view = PuzzleView(self.signals)

        self.stack.addWidget(self.home_view)    # index 0
        self.stack.addWidget(self.gallery_view) # index 1
        self.stack.addWidget(self.puzzle_view)  # index 2

        self._wire_routes()

    def _wire_routes(self):
        self.signals.route_to_home.connect(lambda: self.stack.setCurrentIndex(0))
        self.signals.route_to_gallery.connect(lambda: self.stack.setCurrentIndex(1))
        self.signals.route_to_puzzle.connect(lambda: self.stack.setCurrentIndex(2))