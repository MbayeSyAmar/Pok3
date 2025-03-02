from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt

class BoardCard(QWidget):
    clicked = pyqtSignal(int, str)

    def __init__(self, board_id, title, background):
        super().__init__()
        self.board_id = board_id
        self.title = title
        self.background = background
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        background_label = QLabel()
        pixmap = QPixmap(self.background)
        background_label.setPixmap(pixmap.scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(background_label)

        title_label = QLabel(self.title)
        title_label.setObjectName("board-card-title")
        layout.addWidget(title_label)

        self.setLayout(layout)
        self.setFixedSize(200, 120)
        self.setObjectName("board-card")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.board_id, self.title)