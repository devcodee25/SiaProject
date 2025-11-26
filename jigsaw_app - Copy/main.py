from PySide6.QtWidgets import QApplication
from app.router import JigsawApp

def main():
    app = QApplication([])
    win = JigsawApp()
    win.show()
    app.exec()

if __name__ == "__main__":
    main()