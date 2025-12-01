import sys
import os
import requests

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QWidget, QListWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QTextEdit, QFrame, QLabel,
    QSizePolicy, QStackedLayout
)

API_KEY = "f0af58dddc5b6907cb7373b05c6c7d82"
BASE_URL = "https://api.themoviedb.org/3"

def get_movie_data(title):
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": title}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("results"):
        movie = data["results"][0]
        return {
            "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}",
            "description": movie["overview"]
        }
    return {"poster": "", "description": "No description available."}

def get_tv_data(title):
    url = f"{BASE_URL}/search/tv"
    params = {"api_key": API_KEY, "query": title}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("results"):
        show = data["results"][0]
        return {
            "poster": f"https://image.tmdb.org/t/p/w500{show['poster_path']}",
            "description": show["overview"]
        }
    return {"poster": "", "description": "No description available."}


class MovieHub(QWidget):
    def __init__(self):
        super().__init__()

        self.base_path = os.path.dirname(os.path.abspath(__file__))

        # Movies fetched via API
        self.movies = {
            "Avengers": get_movie_data("Avengers"),
            "Avatar": get_movie_data("Avatar"),
            "John Wick": get_movie_data("John Wick"),
            "The Batman": get_movie_data("The Batman"),
            "Spiderman": get_movie_data("Spiderman"),
            "Zootopia": get_movie_data("Zootopia"),
            "Jujutsu Kaisen 0": get_movie_data("Jujutsu Kaisen 0"),
            'Demon Slayer: Mugen Train': get_movie_data("Demon Slayer: Mugen Train"),
            "KPop Demon Hunters": get_movie_data("KPop Demon Hunters"),
            "Wildcat": get_movie_data("Wildcat"),
            "Superman": get_movie_data("Superman"),
            "F1": get_movie_data("F1"),
            "How to Train Your Dragon": get_movie_data("How to Train Your Dragon"),
            "Your Name": get_movie_data("Your Name"),
            "Lilo & Stitch": get_movie_data("Lilo & Stitch")
        }

        # TV Shows fetched via API
        self.tv_shows = {
            "Breaking Bad": get_tv_data("Breaking Bad"),
            "Stranger Things": get_tv_data("Stranger Things"),
            "The Office": get_tv_data("The Office"),
            "Game of Thrones": get_tv_data("Game of Thrones"),
            "The Mandalorian": get_tv_data("The Mandalorian"),
            "The Simpsons": get_tv_data("The Simpsons"),
            "NCIS": get_tv_data("NCIS"),
            "The Witcher": get_tv_data("The Witcher"),
            "Family Guy": get_tv_data("Family Guy"),
            "Friends": get_tv_data("Friends"),
            "Hazbin Hotel": get_tv_data("Hazbin Hotel"),
            "Arcane": get_tv_data("Arcane"),
            "Loki": get_tv_data("Loki"),
            "WandaVision": get_tv_data("WandaVision"),
            "The Flash": get_tv_data("The Flash")
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
        btn_tv.clicked.connect(self.show_tv_shows)

        for btn in (btn_home, btn_movies, btn_tv):
            btn.setFixedHeight(45)

        sidebar.addWidget(btn_home)
        sidebar.addWidget(btn_movies)
        sidebar.addWidget(btn_tv)
        sidebar.addStretch()
        sidebar.addWidget(btn_exit)

        root.addWidget(sidebar_frame)

        self.stack = QStackedLayout()

        # Home layout
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

        # Movies layout
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

        # TV Shows layout
        tv_layout = QHBoxLayout()
        self.tv_list = QListWidget()
        self.tv_list.addItems(list(self.tv_shows.keys()))
        self.tv_list.setMinimumWidth(280)
        self.tv_list.itemClicked.connect(self.show_tv_details)
        tv_layout.addWidget(self.tv_list)

        tv_details = QVBoxLayout()
        self.tv_poster = QLabel("Poster")
        self.tv_poster.setObjectName("poster")
        self.tv_poster.setFixedSize(400, 600)
        self.tv_poster.setAlignment(Qt.AlignCenter)

        self.tv_title = QLabel("")
        self.tv_title.setObjectName("titleLabel")
        self.tv_title.setStyleSheet("margin-top: 10px;")
        self.tv_title.setAlignment(Qt.AlignCenter)

        self.tv_description = QTextEdit()
        self.tv_description.setReadOnly(True)
        self.tv_description.setFixedHeight(100)

        tv_details.addWidget(self.tv_poster, alignment=Qt.AlignCenter)
        tv_details.addWidget(self.tv_title)
        tv_details.addWidget(self.tv_description)

        tv_layout.addLayout(tv_details)
        tv_widget = QWidget()
        tv_widget.setLayout(tv_layout)
        self.stack.addWidget(tv_widget)

        root.addLayout(self.stack)
        self.setLayout(root)

        self.show_home()

    def show_home(self):
        self.stack.setCurrentIndex(0)

        banner_path = os.path.join(self.base_path, "logo", "logo.jpg")
        pix = QPixmap(banner_path)
        if pix.isNull():
            self.banner.setText("Banner Not Found")
            return

        w = self.width() - 180  
        h = 600
        scaled = pix.scaled(w, h, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        x = (scaled.width() - w) // 2
        y = (scaled.height() - h) // 2
        cropped = scaled.copy(x, y, w, h)
        self.banner.setPixmap(cropped)

        self.welcome.setPlainText(
            "🎬 Welcome to Movies Hub!\n\n"
            "Browse your favorite movies and TV shows with a clean cinema-style interface."
        )

    def show_movies(self):
        self.stack.setCurrentIndex(1)
        self.title.setText("Select a movie")
        self.description.hide()
        self.poster.clear()
        self.poster.setText("")

        if self.list.count() > 0:
            first_item = self.list.item(0)
            self.list.setCurrentItem(first_item)
            self.show_details(first_item)

    def show_tv_shows(self):
        self.stack.setCurrentIndex(2)
        self.tv_title.setText("Select a TV Show")
        self.tv_description.hide()
        self.tv_poster.clear()
        self.tv_poster.setText("")

        if self.tv_list.count() > 0:
            first_item = self.tv_list.item(0)
            self.tv_list.setCurrentItem(first_item)
            self.show_tv_details(first_item)

    def show_details(self, item):
        movie_name = item.text()
        self.title.setText(movie_name)
        self.description.show()

        data = self.movies.get(movie_name)
        if data:
            self.set_poster_image(data["poster"], self.poster)
            self.description.setPlainText(data["description"])
        else:
            self.poster.setText("No Image")
            self.description.setPlainText("No description available.")

    def show_tv_details(self, item):
        show_name = item.text()
        self.tv_title.setText(show_name)
        self.tv_description.show()

        data = self.tv_shows.get(show_name)
        if data:
            self.set_poster_image(data["poster"], self.tv_poster)
            self.tv_description.setPlainText(data["description"])
        else:
            self.tv_poster.setText("No Image")
            self.tv_description.setPlainText("No description available.")

    def set_poster_image(self, image_path, label):
        if image_path.startswith("http"):
            response = requests.get(image_path)
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
        else:
            full_path = os.path.join(self.base_path, image_path)
            pixmap = QPixmap(full_path)

        if pixmap.isNull():
            label.setText("Image Not Found")
            return

        w, h = label.width(), label.height()
        scaled = pixmap.scaled(w, h, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        x = (scaled.width() - w) // 2
        y = (scaled.height() - h) // 2
        cropped = scaled.copy(x, y, w, h)
        label.setPixmap(cropped)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MovieHub()
    win.show()
    sys.exit(app.exec_())
