from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QMessageBox,
    QHBoxLayout,
    QFrame,
    QPushButton,
    QProgressBar,
)
from PySide6.QtCore import Qt, QTimer
from app.widgets.nav_bar import NavBar
from app.widgets.tile_widget import TileWidget
from core.puzzle_board import PuzzleBoard
from core.image_loader import load_pixmap
from core.game_state import GameState
from core.models import PuzzleConfig

class PuzzleView(QWidget):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals
        self.board: PuzzleBoard | None = None
        self.state = GameState()
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._handle_tick)
        self.current_config: PuzzleConfig | None = None
        self.selected_index: int | None = None
        self.tile_widgets: list[TileWidget] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.toolbar = NavBar("Puzzle", on_home=self.signals.route_to_home.emit,
                              on_back=self.signals.route_to_gallery.emit)
        root.addWidget(self.toolbar)

        info_strip = QFrame()
        info_strip.setObjectName("infoStrip")
        info_layout = QHBoxLayout(info_strip)
        info_layout.setContentsMargins(16, 8, 16, 8)
        info_layout.setSpacing(24)

        self.lbl_moves = QLabel("Moves: 0")
        self.lbl_timer = QLabel("Time: 00:00")
        self.lbl_status = QLabel("Pick any tile to begin.")
        info_layout.addWidget(self.lbl_moves)
        info_layout.addWidget(self.lbl_timer)
        info_layout.addWidget(self.lbl_status, 1)
        root.addWidget(info_strip)

        content = QHBoxLayout()
        content.setContentsMargins(16, 12, 16, 16)
        content.setSpacing(18)
        root.addLayout(content, 1)

        board_frame = QFrame()
        board_frame.setObjectName("boardFrame")
        board_layout = QVBoxLayout(board_frame)
        board_layout.setContentsMargins(12, 12, 12, 12)
        board_layout.setSpacing(6)

        self.grid_container = QWidget()
        self.grid = QGridLayout(self.grid_container)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(6)
        board_layout.addWidget(self.grid_container, 1)
        content.addWidget(board_frame, 3)

        self.side_panel = self._build_side_panel()
        content.addWidget(self.side_panel, 1)

        signals.start_puzzle.connect(self._start_game)
        signals.route_to_gallery.connect(self._handle_exit)
        signals.route_to_home.connect(self._handle_exit)

    def _build_side_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("infoPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        self.preview_label = QLabel()
        self.preview_label.setObjectName("previewImage")
        self.preview_label.setFixedSize(320, 180)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("background: #111; color: #fff;")
        self.preview_label.setScaledContents(True)

        self.lbl_meta = QLabel("")
        self.lbl_meta.setObjectName("metaLabel")
        self.lbl_meta.setWordWrap(True)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        btn_shuffle = QPushButton("Reshuffle tiles")
        btn_shuffle.clicked.connect(self._reshuffle_current)
        btn_gallery = QPushButton("Pick another artwork")
        btn_gallery.clicked.connect(self.signals.route_to_gallery.emit)

        layout.addWidget(self.preview_label)
        layout.addSpacing(8)
        layout.addWidget(self.lbl_meta)
        layout.addSpacing(4)
        layout.addWidget(self.progress)
        layout.addStretch(1)
        layout.addWidget(btn_shuffle)
        layout.addWidget(btn_gallery)
        return panel

    def _start_game(self, config: PuzzleConfig):
        self.current_config = config
        self.toolbar.set_title(config.title)

        target_w, target_h = 960, 540  # 16:9 canvas
        pm = load_pixmap(config.image_path, target_w, target_h)
        self.preview_label.setPixmap(pm.scaled(320, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.board = PuzzleBoard(pm, rows=config.rows, cols=config.cols)
        self.board.slice_tiles()
        self.board.shuffle()
        self.state.configure(config.rows, config.cols)
        self.lbl_moves.setText("Moves: 0")
        self.lbl_timer.setText("Time: 00:00")
        self.lbl_status.setText("Select any tile, then another to swap.")
        self.selected_index = None
        self.tile_widgets.clear()
        self.progress.setValue(0)
        self.lbl_meta.setText(f"{config.piece_count} pieces · {config.rows} × {config.cols}")

        self.timer.stop()
        self.timer.start()

        # Build grid
        self._populate_grid()

    def _populate_grid(self):
        # Clear grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        rows, cols = self.board.grid_size()
        tile_w = self.board.pixmap.width() // cols
        tile_h = self.board.pixmap.height() // rows

        idx = 0
        for r in range(rows):
            for c in range(cols):
                tile = TileWidget(idx, tile_w, tile_h)
                pm = self.board.get_tile_pixmap(idx)
                tile.setPixmap(pm)
                tile.clicked.connect(self._tile_clicked)
                self.grid.addWidget(tile, r, c)
                self.tile_widgets.append(tile)
                idx += 1

    def _tile_clicked(self, index: int):
        if not self.board:
            return

        if self.selected_index is None:
            self.selected_index = index
            self._set_tile_selected(index, True)
            self.lbl_status.setText(f"Selected tile {index+1}. Choose another tile to swap.")
            return

        if index == self.selected_index:
            self._set_tile_selected(index, False)
            self.lbl_status.setText("Selection cleared.")
            self.selected_index = None
            return

        # Swap
        first = self.selected_index
        self._set_tile_selected(first, False)
        self.board.swap(first, index)
        self.state.increment_move()
        self.lbl_moves.setText(f"Moves: {self.state.moves}")
        self.selected_index = None
        self.lbl_status.setText("Great swap! Keep going.")

        # Refresh grid tiles
        self._refresh_tiles()
        self._update_progress()

        # Check solved
        if self.board.is_solved():
            self.timer.stop()
            title = self.current_config.title if self.current_config else "this puzzle"
            QMessageBox.information(
                self,
                "Puzzle solved",
                f"You solved {title} in {self.state.moves} moves and {self.state.formatted_time()}.",
            )
            self.signals.route_to_gallery.emit()

    def _refresh_tiles(self):
        idx = 0
        for i in range(self.grid.count()):
            w = self.grid.itemAt(i).widget()
            if not w:
                continue
            pm = self.board.get_tile_pixmap(idx)
            w.setPixmap(pm)
            idx += 1

    def _set_tile_selected(self, index: int, selected: bool):
        if 0 <= index < len(self.tile_widgets):
            self.tile_widgets[index].set_selected(selected)

    def _update_progress(self):
        if not self.board:
            self.progress.setValue(0)
            return
        total = len(self.board.order)
        aligned = sum(1 for idx, tile_idx in enumerate(self.board.order) if idx == tile_idx)
        percent = int((aligned / total) * 100)
        self.progress.setValue(percent)

    def _handle_tick(self):
        self.state.tick()
        self.lbl_timer.setText(f"Time: {self.state.formatted_time()}")

    def _handle_exit(self):
        self.timer.stop()
        self.selected_index = None

    def _reshuffle_current(self):
        if not self.board or not self.current_config:
            return
        self.board.shuffle()
        self.state.reset_moves_only()
        self.lbl_moves.setText("Moves: 0")
        self.selected_index = None
        self._refresh_tiles()
        self._update_progress()
        self.lbl_status.setText("Tiles reshuffled. Try a new strategy!")