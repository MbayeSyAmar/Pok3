from PyQt5.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QPushButton, QVBoxLayout, QLabel, QInputDialog
from PyQt5.QtCore import Qt
from components.list_widget import ListWidget

class BoardView(QWidget):
    def __init__(self, db, show_board_list_callback):
        super().__init__()
        self.db = db
        self.show_board_list_callback = show_board_list_callback
        self.lists = []
        self.current_board_id = None
        self.current_board_title = None
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.board_header = QWidget()
        self.board_header.setObjectName("board-header")
        header_layout = QHBoxLayout(self.board_header)
        self.board_title = QLabel()
        self.board_title.setObjectName("board-title")
        header_layout.addWidget(self.board_title)
        main_layout.addWidget(self.board_header)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.scroll_content = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(15)
        self.scroll_layout.setContentsMargins(15, 15, 15, 15)
        self.scroll_layout.setAlignment(Qt.AlignLeft)
        
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)
        
        self.setLayout(main_layout)
        
    def load_board(self, board_id, board_title):
        self.current_board_id = board_id
        self.current_board_title = board_title
        self.board_title.setText(board_title)
        self.clear_lists()
        lists = self.db.get_lists(board_id)
        for list_data in lists:
            list_widget = ListWidget(list_data['id'], list_data['title'], self.db)
            list_widget.card_moved.connect(self.on_card_moved)
            self.lists.append(list_widget)
            self.scroll_layout.addWidget(list_widget)
        
        add_list_button = QPushButton("+ Ajouter une liste")
        add_list_button.setObjectName("add-list-button")
        add_list_button.clicked.connect(self.create_new_list)
        self.scroll_layout.addWidget(add_list_button)
        
    def clear_lists(self):
        for list_widget in self.lists:
            self.scroll_layout.removeWidget(list_widget)
            list_widget.deleteLater()
        self.lists.clear()
        
    def create_new_list(self):
        title, ok = QInputDialog.getText(self, "Nouvelle liste", "Nom de la liste:")
        if ok and title:
            new_list_id = self.db.create_list(title, len(self.lists), self.current_board_id)
            new_list = ListWidget(new_list_id, title, self.db)
            new_list.card_moved.connect(self.on_card_moved)
            self.lists.append(new_list)
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, new_list)
            
    def on_card_moved(self, card_id, new_list_id):
        # Recharger toutes les listes pour refléter les changements
        for list_widget in self.lists:
            list_widget.load_cards()

