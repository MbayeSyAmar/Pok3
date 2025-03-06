from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal

class Sidebar(QWidget):
    show_boards_requested = pyqtSignal()
    show_calendar_requested = pyqtSignal()
    show_timeline_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QLabel("Menu")
        title.setObjectName("sidebar-title")
        layout.addWidget(title)

        boards_button = QPushButton("📋  Tableaux")  # Ajout d'espaces après l'emoji
        boards_button.setObjectName("sidebar-button")
        boards_button.clicked.connect(self.show_boards_requested.emit)
        layout.addWidget(boards_button)

        calendar_button = QPushButton("📅  Calendrier")
        calendar_button.setObjectName("sidebar-button")
        calendar_button.clicked.connect(self.show_calendar_requested.emit)
        layout.addWidget(calendar_button)

        timeline_button = QPushButton("⏱️  Chronologie")
        timeline_button.setObjectName("sidebar-button")
        timeline_button.clicked.connect(self.show_timeline_requested.emit)
        layout.addWidget(timeline_button)

        layout.addStretch()

        self.setLayout(layout)
        self.setObjectName("sidebar")

