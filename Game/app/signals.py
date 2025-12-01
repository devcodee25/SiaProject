from PySide6.QtCore import QObject, Signal

from core.models import PuzzleConfig

class AppSignals(QObject):
    route_to_home = Signal()
    route_to_gallery = Signal()
    route_to_puzzle = Signal()

    # Game-related
    start_puzzle = Signal(object)  # PuzzleConfig
    puzzle_solved = Signal()