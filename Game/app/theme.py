from PySide6.QtWidgets import QApplication


def apply_theme():
    """Apply EntertainHub pastel palette across all widgets."""
    style = """
    QWidget {
        font-family: 'Segoe UI', 'Poppins', Arial;
        font-size: 14px;
        color: #2b1f4b;
        background: #fdf7ff;
    }
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #fef1ff, stop:1 #e2f4ff);
    }
    QPushButton {
        border-radius: 10px;
        padding: 10px 18px;
        border: none;
        font-weight: 600;
        color: #fff;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #ff9acd, stop:1 #a372ff);
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #ffb0d7, stop:1 #b58bff);
    }
    QPushButton#primaryButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #ffd18f, stop:1 #ff9bb0);
        color: #4a2b63;
    }
    QLabel#title {
        font-size: 30px;
        font-weight: 700;
        color: #2b1f4b;
    }
    QLabel#subtitle {
        font-size: 16px;
        color: #6f5c98;
    }
    QFrame#toolbar {
        background: rgba(255, 255, 255, 0.85);
        border-bottom: 1px solid #f0dcff;
    }
    QFrame#boardFrame,
    QFrame#galleryCard {
        background: #ffffff;
        border-radius: 18px;
        border: 1px solid #f1d8ff;
        box-shadow: 0px 12px 24px rgba(80, 41, 125, 0.08);
    }
    QLabel#galleryPreview {
        border-top-left-radius: 18px;
        border-top-right-radius: 18px;
        background: #f8f6ff;
    }
    QLabel#cardTitle {
        font-size: 18px;
        font-weight: 600;
        color: #2b1f4b;
    }
    QLabel#cardSubtitle {
        color: #7b6e9f;
    }
    QFrame#infoPanel {
        background: #ffffff;
        border-radius: 18px;
        border: 1px solid #f1d8ff;
        color: #2b1f4b;
    }
    QLabel#metaLabel {
        color: #6c5a8b;
    }
    QLabel#previewImage {
        border-radius: 14px;
        background: #f7f3ff;
    }
    QLabel#tileWidget {
        border-radius: 8px;
        border: 2px solid transparent;
        background: #ffffff;
        box-shadow: inset 0 0 0 1px #f2defd;
    }
    QLabel#tileWidget[selected="true"] {
        border-color: #ff9acd;
        box-shadow: 0 0 12px rgba(255, 154, 205, 0.6);
    }
    QProgressBar {
        border-radius: 10px;
        border: 1px solid #f1d8ff;
        background: #f8f4ff;
        color: #4a2b63;
    }
    QProgressBar::chunk {
        border-radius: 10px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #ffb1d1, stop:1 #b48dff);
    }
    QFrame#infoStrip {
        background: rgba(255, 255, 255, 0.75);
        border-bottom: 1px solid #f1d8ff;
    }
    QLabel {
        color: #2b1f4b;
    }
    """
    QApplication.instance().setStyleSheet(style)