from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class Board(QWidget):
    def __init__(self, board_id, title):
        super().__init__()
        self.board_id = board_id
        self.title = title
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        layout.addWidget(title_label)
        
        open_btn = QPushButton("Ouvrir")
        open_btn.clicked.connect(self.open_board)
        layout.addWidget(open_btn)
        
        self.setLayout(layout)
    
    def open_board(self):
        # TODO: Implémenter l'ouverture du tableau
        print(f"Ouverture du tableau {self.title}")

class BoardList(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
    
    def add_board(self, board):
        self.layout.addWidget(board)

