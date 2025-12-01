import os
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QSizePolicy,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from app.assets import IMAGE_CATALOG
from app.widgets.nav_bar import NavBar
from core.models import PuzzleConfig

class GalleryView(QWidget):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        toolbar = NavBar("Gallery", on_home=self.signals.route_to_home.emit,
                         on_back=self.signals.route_to_home.emit)
        root.addWidget(toolbar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        root.addWidget(self.scroll, 1)

        self._build_gallery()

    def _build_gallery(self):
        content = QWidget()
        grid = QGridLayout(content)
        grid.setContentsMargins(32, 24, 32, 24)
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(18)

        if not IMAGE_CATALOG:
            empty = QLabel("No artwork found. Drop 10 images into the assets/images folder.")
            empty.setAlignment(Qt.AlignCenter)
            grid.addWidget(empty, 0, 0)
            self.scroll.setWidget(content)
            return

        cards_per_row = 3
        for i, config in enumerate(IMAGE_CATALOG):
            card = self._create_card(config)
            r, c = divmod(i, cards_per_row)
            grid.addWidget(card, r, c)

        self.scroll.setWidget(content)

    def _create_card(self, config: PuzzleConfig) -> QWidget:
        frame = QFrame()
        frame.setObjectName("galleryCard")
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        preview = QLabel()
        preview.setObjectName("galleryPreview")
        preview.setFixedSize(320, 200)
        preview.setAlignment(Qt.AlignCenter)
        preview.setScaledContents(False)

        if os.path.exists(config.image_path):
            pm = QPixmap(config.image_path)
            if not pm.isNull():
                scaled = pm.scaled(
                    preview.width(),
                    preview.height(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation,
                )
                preview.setPixmap(scaled)
            else:
                preview.setText("Image missing")
        else:
            preview.setText("Image missing")

        body = QFrame()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(16, 12, 16, 16)
        body_layout.setSpacing(6)

        title = QLabel(config.title)
        title.setObjectName("cardTitle")
        subtitle = QLabel(f"{config.piece_count} pieces · {config.rows} × {config.cols}")
        subtitle.setObjectName("cardSubtitle")

        cta_row = QHBoxLayout()
        cta_row.setSpacing(8)
        cta_row.addStretch(1)
        btn = QPushButton("Start puzzle")
        btn.setObjectName("primaryButton")
        btn.clicked.connect(lambda _, cfg=config: self._start(cfg))
        cta_row.addWidget(btn)

        body_layout.addWidget(title)
        body_layout.addWidget(subtitle)
        body_layout.addSpacing(4)
        body_layout.addLayout(cta_row)

        layout.addWidget(preview)
        layout.addWidget(body)

        return frame

    def _start(self, config: PuzzleConfig):
        self.signals.start_puzzle.emit(config)
        self.signals.route_to_puzzle.emit()