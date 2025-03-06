from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal

class Header(QWidget):
    logout_requested = pyqtSignal()
    notification_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        menu_button = QPushButton("☰")  # Menu hamburger plus visible
        menu_button.setObjectName("menu-button")
        menu_button.clicked.connect(self.parent().toggle_sidebar)
        layout.addWidget(menu_button)

        logo = QLabel("PyTrello")
        logo.setObjectName("header-logo")
        layout.addWidget(logo)

        layout.addStretch()

        self.board_title = QLabel()
        self.board_title.setObjectName("board-title")
        layout.addWidget(self.board_title)

        layout.addStretch()

        notification_button = QPushButton("🔔")  # Cloche plus visible
        notification_button.setObjectName("notification-button")
        notification_button.clicked.connect(self.notification_requested.emit)
        layout.addWidget(notification_button)

        self.user_info = QLabel()
        self.user_info.setObjectName("user-info")
        layout.addWidget(self.user_info)

        logout_button = QPushButton("Déconnexion")
        logout_button.setObjectName("logout-button")
        logout_button.clicked.connect(self.logout_requested.emit)
        layout.addWidget(logout_button)

        self.setLayout(layout)
        self.setObjectName("main-header")


    def update_user_info(self, username):
        self.user_info.setText(f"Connecté en tant que : {username}")

    def clear_user_info(self):
        self.user_info.clear()

    def set_board_title(self, title):
        self.board_title.setText(title)

    def clear_board_title(self):
        self.board_title.clear()

    def set_view_title(self, title):
        self.board_title.setText(title)

