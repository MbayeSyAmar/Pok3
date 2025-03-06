from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import pyqtSignal, Qt

class BoardCard(QWidget):
    clicked = pyqtSignal(int, str)

    def __init__(self, board_id, title, background=None):
        super().__init__()
        self.board_id = board_id
        self.title = title
        self.background = background
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Créer un fond coloré au lieu d'utiliser une image
        background_label = QLabel()
        background_label.setFixedSize(200, 100)
        background_label.setStyleSheet(f"background-color: #5E35B1; border-radius: 6px 6px 0 0;")
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

