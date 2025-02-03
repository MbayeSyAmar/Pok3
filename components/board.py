from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QInputDialog
from PyQt5.QtCore import pyqtSignal
from components.list import List

class Board(QWidget):
    board_clicked = pyqtSignal(int)
    board_deleted = pyqtSignal(int)

    def __init__(self, board_id, title, db):
        super().__init__()
        self.board_id = board_id
        self.title = title
        self.db = db
        self.init_ui()

    def init_ui(self):
        """Initialise l'interface utilisateur du tableau."""
        
        layout = QVBoxLayout()
        
        # En-tête du tableau
        header = QHBoxLayout()
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.addWidget(self.title_label)
        
        open_button = QPushButton("Ouvrir")
        open_button.clicked.connect(self.open_board)
        header.addWidget(open_button)

        edit_button = QPushButton("Modifier")
        edit_button.clicked.connect(self.edit_board)
        header.addWidget(edit_button)

        delete_button = QPushButton("Supprimer")
        delete_button.clicked.connect(self.delete_board)
        header.addWidget(delete_button)
        
        layout.addLayout(header)
        
        self.setLayout(layout)
        
    def open_board(self):
        """Émet un signal lorsque le tableau est ouvert."""
        self.board_clicked.emit(self.board_id)

    def edit_board(self):
        """Modifie le titre du tableau."""
        new_title, ok = QInputDialog.getText(self, "Modifier le tableau", "Nouveau titre:", text=self.title)
        if ok and new_title:
            self.db.update_board(self.board_id, new_title)
            self.title = new_title
            self.title_label.setText(new_title)

    def delete_board(self):
        """Supprime le tableau."""
        self.db.delete_board(self.board_id)
        self.board_deleted.emit(self.board_id)

class BoardView(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.lists = []
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur de la vue du tableau."""
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
    def load_lists(self, board_id):
        """Charge les listes du tableau."""
        self.clear_lists()
        lists = self.db.get_lists(board_id)
        for list_data in lists:
            list_widget = List(list_data['id'], list_data['title'], self.db)
            self.lists.append(list_widget)
            self.layout.addWidget(list_widget)
        
        # Ajouter un bouton pour créer une nouvelle liste
        add_list_button = QPushButton("+ Ajouter une liste")
        add_list_button.clicked.connect(lambda: self.create_new_list(board_id))
        self.layout.addWidget(add_list_button)
        
    def clear_lists(self):
        """Efface toutes les listes de la vue."""
        for list_widget in self.lists:
            self.layout.removeWidget(list_widget)
            list_widget.deleteLater()
        self.lists.clear()
        
    def create_new_list(self, board_id):
        """Crée une nouvelle liste dans le tableau."""
        title, ok = QInputDialog.getText(self, "Nouvelle liste", "Titre de la liste:")
        if ok and title:
            position = len(self.lists)
            self.db.create_list(title, position, board_id)
            self.load_lists(board_id)

