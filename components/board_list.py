from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal

class BoardList(QWidget):
    board_selected = pyqtSignal(int)

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.boards = []
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Mes tableaux")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(title)

        self.boards_layout = QVBoxLayout()
        self.layout.addLayout(self.boards_layout)

        add_board_button = QPushButton("+ Créer un nouveau tableau")
        add_board_button.clicked.connect(self.create_new_board)
        self.layout.addWidget(add_board_button)

        self.setLayout(self.layout)

    def load_boards(self, user_id):
        self.clear_boards()
        boards = self.db.get_boards(user_id)
        for board in boards:
            board_widget = BoardWidget(board['id'], board['title'], self.db)
            board_widget.board_clicked.connect(self.board_selected.emit)
            self.boards.append(board_widget)
            self.boards_layout.addWidget(board_widget)

    def clear_boards(self):
        for board in self.boards:
            self.boards_layout.removeWidget(board)
            board.deleteLater()
        self.boards.clear()

    def create_new_board(self):
        new_board_widget = NewBoardWidget(self.db)
        new_board_widget.board_created.connect(self.add_board)
        self.boards_layout.addWidget(new_board_widget)

    def add_board(self, board_id, title):
        board_widget = BoardWidget(board_id, title, self.db)
        board_widget.board_clicked.connect(self.board_selected.emit)
        self.boards.append(board_widget)
        self.boards_layout.addWidget(board_widget)

class BoardWidget(QWidget):
    board_clicked = pyqtSignal(int)

    def __init__(self, board_id, title, db):
        super().__init__()
        self.board_id = board_id
        self.title = title
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(title_label)

        open_button = QPushButton("Ouvrir")
        open_button.clicked.connect(self.open_board)
        layout.addWidget(open_button)

        self.setLayout(layout)

    def open_board(self):
        self.board_clicked.emit(self.board_id)

class NewBoardWidget(QWidget):
    board_created = pyqtSignal(int, str)

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Titre du nouveau tableau")
        layout.addWidget(self.title_input)

        create_button = QPushButton("Créer")
        create_button.clicked.connect(self.create_board)
        layout.addWidget(create_button)

        self.setLayout(layout)

    def create_board(self):
        title = self.title_input.text()
        if title:
            board_id = self.db.create_board(title, 1)  # Assuming user_id is 1 for simplicity
            self.board_created.emit(board_id, title)
            self.deleteLater()

