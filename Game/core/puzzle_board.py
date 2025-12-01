import random
from typing import List, Tuple
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QRect

class PuzzleBoard:
    def __init__(self, pixmap: QPixmap, rows: int = 4, cols: int = 6):
        self.rows = rows
        self.cols = cols
        self.pixmap = pixmap
        self.tiles: List[QPixmap] = []
        self.order: List[int] = []  # current tile order
        self.original_order: List[int] = []  # 0..n-1

    def slice_tiles(self):
        w = self.pixmap.width() // self.cols
        h = self.pixmap.height() // self.rows
        self.tiles.clear()
        self.original_order = list(range(self.rows * self.cols))
        for r in range(self.rows):
            for c in range(self.cols):
                rect = QRect(c * w, r * h, w, h)
                self.tiles.append(self.pixmap.copy(rect))
        self.order = self.original_order.copy()

    def shuffle(self):
        random.shuffle(self.order)

    def swap(self, i: int, j: int):
        self.order[i], self.order[j] = self.order[j], self.order[i]

    def is_solved(self) -> bool:
        return self.order == self.original_order

    def get_tile_pixmap(self, position_index: int) -> QPixmap:
        original_index = self.order[position_index]
        return self.tiles[original_index]

    def grid_size(self) -> Tuple[int, int]:
        return self.rows, self.cols