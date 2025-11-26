import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QWidget, QListWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QTextEdit, QFrame, QLabel,
    QSizePolicy, QStackedLayout
)


class MovieHub(QWidget):
    def __init__(self):
        super().__init__()

        self.movies = {
            "Avengers": {
                "poster": "posters/avengers.jpg",
                "description": "Earth's mightiest heroes join forces to stop Loki and his alien army."
            },
            "Avatar": {
                "poster": "posters/avatar.jpg",
                "description": "A marine on an alien planet becomes part of a tribal society."
            },
            "John Wick": {
                "poster": "posters/johnwick.jpg",
                "description": "An ex-hitman comes out of retirement to track down gangsters."
            },
            "The Batman": {
                "poster": "posters/batman.jpg",
                "description": "Batman investigates corruption and faces the Riddler."
            },
            "Spiderman": {
                "poster": "posters/spiderman.jpg",
                "description": "Peter Parker faces new villains while balancing life and heroism."
            }
        }

        self.setWindowTitle("🎬 Movies Hub")
        self.resize(1050, 600)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #fef1ff, stop:1 #e2f4ff);
                color: #2b1f4b;
                font-family: 'Segoe UI', 'Poppins', Arial;
                font-size: 14px;
            }
            QFrame#sidebar {
                background: rgba(255, 255, 255, 0.65);
                border-right: 1px solid #f1d8ff;
            }
            QListWidget {
                background: rgba(255, 255, 255, 0.85);
                border: 1px solid #f1d8ff;
                border-radius: 16px;
                padding: 8px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 10px;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #ffb1d1, stop:1 #b48dff);
                color: #fff;
            }
            QPushButton {
                background: #ffffff;
                border: 1px solid #f1d8ff;
                border-radius: 12px;
                padding: 10px;
                font-weight: 600;
                color: #5a4a80;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #ffd6ec, stop:1 #c9a7ff);
                color: #fff;
                border-color: transparent;
            }
            QLabel#poster, QLabel#banner {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 18px;
                border: 1px solid #f1d8ff;
            }
            QTextEdit {
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #f1d8ff;
                border-radius: 16px;
                padding: 12px;
                font-size: 16px;
                color: #4a2b63;
            }
            QLabel#titleLabel {
                font-size: 28px;
                font-weight: 700;
                color: #2b1f4b;
            }
            QLabel#sectionHeader {
                font-size: 18px;
                color: #6f5c98;
            }
        """)

        root = QHBoxLayout()
        root.setSpacing(0)

        sidebar = QVBoxLayout()
        sidebar.setAlignment(Qt.AlignTop)

        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("sidebar")
        sidebar_frame.setLayout(sidebar)
        sidebar_frame.setFixedWidth(180)

        btn_home = QPushButton("🏠 Home")
        btn_movies = QPushButton("🎞 Movies")
        btn_tv = QPushButton("📺 TV Shows")
        btn_exit = QPushButton("❌ Exit")

        btn_exit.clicked.connect(self.close)
        btn_home.clicked.connect(self.show_home)
        btn_movies.clicked.connect(self.show_movies)

        for btn in (btn_home, btn_movies, btn_tv):
            btn.setFixedHeight(45)

        sidebar.addWidget(btn_home)
        sidebar.addWidget(btn_movies)
        sidebar.addWidget(btn_tv)
        sidebar.addStretch()
        sidebar.addWidget(btn_exit)

        root.addWidget(sidebar_frame)

        self.stack = QStackedLayout()

        home_layout = QVBoxLayout()
        self.banner = QLabel()
        self.banner.setObjectName("banner")
        self.banner.setAlignment(Qt.AlignCenter)
        self.banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        home_layout.addWidget(self.banner)

        self.welcome = QTextEdit()
        self.welcome.setReadOnly(True)
        self.welcome.setFixedHeight(100)
        home_layout.addWidget(self.welcome)

        home_widget = QWidget()
        home_widget.setLayout(home_layout)
        self.stack.addWidget(home_widget)

        movie_layout = QHBoxLayout()

        self.list = QListWidget()
        self.list.addItems(list(self.movies.keys()))
        self.list.setMinimumWidth(280)
        self.list.itemClicked.connect(self.show_details)
        movie_layout.addWidget(self.list)

        details = QVBoxLayout()

        self.poster = QLabel("Poster")
        self.poster.setObjectName("poster")
        self.poster.setFixedSize(400, 600)
        self.poster.setAlignment(Qt.AlignCenter)

        self.title = QLabel("")
        self.title.setObjectName("titleLabel")
        self.title.setStyleSheet("margin-top: 10px;")
        self.title.setAlignment(Qt.AlignCenter)

        self.description = QTextEdit()
        self.description.setReadOnly(True)
        self.description.setFixedHeight(100)

        details.addWidget(self.poster, alignment=Qt.AlignCenter)
        details.addWidget(self.title)
        details.addWidget(self.description)

        movie_layout.addLayout(details)

        movie_widget = QWidget()
        movie_widget.setLayout(movie_layout)
        self.stack.addWidget(movie_widget)

        root.addLayout(self.stack)
        self.setLayout(root)

        self.show_home()

    def show_home(self):
        self.stack.setCurrentIndex(0)

        pix = QPixmap("posters/banner.jpg")
        w = self.width() - 180  
        h = 600
        scaled = pix.scaled(w, h, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        x = (scaled.width() - w) // 2
        y = (scaled.height() - h) // 2
        cropped = scaled.copy(x, y, w, h)
        self.banner.setPixmap(cropped)

        self.welcome.setPlainText(
            "🎬 Welcome to Movies Hub!\n\n"
            "Browse your favorite movies with a clean cinema-style interface."
        )

    def show_movies(self):
        self.stack.setCurrentIndex(1)
        self.title.setText("Select a movie")
        self.description.hide()
        self.poster.clear()
        self.poster.setText("")

    def show_details(self, item):
        movie_name = item.text()
        self.title.setText(movie_name)
        self.description.show()

        data = self.movies.get(movie_name)
        if data:
            self.set_poster_image(data["poster"])
            self.description.setPlainText(data["description"])
        else:
            self.poster.setText("No Image")
            self.description.setPlainText("No description available.")

    def set_poster_image(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.poster.setText("Image Not Found")
            return

        w, h = self.poster.width(), self.poster.height()
        scaled = pixmap.scaled(w, h, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        x = (scaled.width() - w) // 2
        y = (scaled.height() - h) // 2
        cropped = scaled.copy(x, y, w, h)
        self.poster.setPixmap(cropped)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MovieHub()
    win.show()
    sys.exit(app.exec_())
