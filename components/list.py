from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QInputDialog
from PyQt5.QtCore import Qt
from components.card import Card

class List(QWidget):
    def __init__(self, list_id, title, db):
        super().__init__()
        self.list_id = list_id
        self.title = title
        self.db = db
        self.cards = []
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.title_label)
        
        self.cards_layout = QVBoxLayout()
        layout.addLayout(self.cards_layout)
        
        add_card_button = QPushButton("+ Ajouter une carte")
        add_card_button.clicked.connect(self.add_new_card)
        layout.addWidget(add_card_button)
        
        self.setLayout(layout)
        self.setFixedWidth(250)
        self.setStyleSheet("background-color: #ebecf0; border-radius: 3px;")
        
        self.load_cards()
        
    def load_cards(self):
        cards = self.db.get_cards(self.list_id)
        for card_data in cards:
            self.add_card(card_data['id'], card_data['title'])
        
    def add_new_card(self):
        title, ok = QInputDialog.getText(self, "Nouvelle carte", "Titre de la carte:")
        if ok and title:
            new_card_id = self.db.create_card(title, "", len(self.cards), self.list_id)
            self.add_card(new_card_id, title)
        
    def add_card(self, card_id, title):
        card = Card(card_id, title, self.db)
        self.cards.append(card)
        self.cards_layout.addWidget(card)

