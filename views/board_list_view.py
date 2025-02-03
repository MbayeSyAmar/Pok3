from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QInputDialog, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal
from components.board_card import BoardCard

class BoardListView(QWidget):
    board_selected = pyqtSignal(int, str)

    def __init__(self, db, show_board_callback):
        super().__init__()
        self.db = db
        self.show_board_callback = show_board_callback
        self.boards = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title = QLabel("Mes tableaux")
        title.setObjectName("page-title")
        main_layout.addWidget(title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_content = QWidget()
        self.boards_layout = QHBoxLayout(scroll_content)
        self.boards_layout.setAlignment(Qt.AlignLeft)
        self.boards_layout.setSpacing(20)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        add_board_button = QPushButton("Créer un nouveau tableau")
        add_board_button.setObjectName("create-board-button")
        add_board_button.clicked.connect(self.create_new_board)
        main_layout.addWidget(add_board_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def load_boards(self, user_id):
        self.clear_boards()
        boards = self.db.get_boards(user_id)
        for board in boards:
            board_card = BoardCard(board['id'], board['title'], board['background'])
            board_card.clicked.connect(self.on_board_clicked)
            self.boards.append(board_card)
            self.boards_layout.addWidget(board_card)

    def clear_boards(self):
        for board in self.boards:
            self.boards_layout.removeWidget(board)
            board.deleteLater()
        self.boards.clear()

    def create_new_board(self):
        title, ok = QInputDialog.getText(self, "Nouveau tableau", "Nom du tableau:")
        if ok and title:
            background = "assets/images/board_backgrounds/default.jpg"  # You can add more options for backgrounds
            board_id = self.db.create_board(title, background, 1)  # Assuming user_id is 1 for simplicity
            board_card = BoardCard(board_id, title, background)
            board_card.clicked.connect(self.on_board_clicked)
            self.boards.append(board_card)
            self.boards_layout.addWidget(board_card)

    def on_board_clicked(self, board_id, board_title):
        self.show_board_callback(board_id, board_title)

