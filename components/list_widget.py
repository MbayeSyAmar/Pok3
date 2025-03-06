from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog, QFrame, QHBoxLayout, QScrollArea, QMenu, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from components.card_widget import CardWidget, CardDetailDialog

class ListWidget(QWidget):
    card_moved = pyqtSignal(int, int)  # card_id, new_list_id
    
    def __init__(self, list_id, title, db):
        super().__init__()
        self.list_id = list_id
        self.title = title
        self.db = db
        self.cards = []
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel(self.title)
        title_label.setObjectName("list-title")
        header_layout.addWidget(title_label)
        
        menu_button = QPushButton("⋮")
        menu_button.setFixedSize(28, 28)
        menu_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #B3B3B3;
                font-size: 18px;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
                color: #FFFFFF;
                border-radius: 4px;
            }
        """)
        menu_button.clicked.connect(self.show_menu)
        header_layout.addWidget(menu_button)
        
        layout.addLayout(header_layout)
        
        # Cards container
        self.cards_widget = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_widget)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(2)
        self.cards_layout.setAlignment(Qt.AlignTop)
        
        # Scroll area for cards
        scroll = QScrollArea()
        scroll.setWidget(self.cards_widget)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        layout.addWidget(scroll)
        
        # Add card button
        add_card_button = QPushButton("+ Ajouter une carte")
        add_card_button.setObjectName("add-card-button")
        add_card_button.clicked.connect(self.add_new_card)
        layout.addWidget(add_card_button)
        
        self.setLayout(layout)
        self.setObjectName("list-widget")
        self.setAcceptDrops(True)
        
        self.load_cards()
        
    def load_cards(self):
        # Effacer les cartes existantes
        for card in self.cards:
            self.cards_layout.removeWidget(card)
            card.deleteLater()
        self.cards.clear()
        
        # Charger les cartes depuis la base de données
        cards = self.db.get_cards(self.list_id)
        for card_data in cards:
            self.add_card(card_data['id'], card_data['title'])
        
    def add_new_card(self):
        title, ok = QInputDialog.getText(self, "Nouvelle carte", "Titre de la carte:")
        if ok and title:
            new_card_id = self.db.create_card(title, "", len(self.cards), None, self.list_id)
            self.add_card(new_card_id, title)
        
    def add_card(self, card_id, title):
        card = CardWidget(card_id, title, self.db)
        card.card_clicked.connect(self.show_card_details)
        card.card_moved.connect(self.card_moved.emit)
        self.cards.append(card)
        self.cards_layout.addWidget(card)
        
    def show_card_details(self, card_id):
        dialog = CardDetailDialog(card_id, self.db)
        if dialog.exec_():
            self.load_cards()  # Recharger les cartes pour refléter les changements
            
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            
    def dropEvent(self, event):
        if event.mimeData().hasText():
            card_id = int(event.mimeData().text())
            
            # Mettre à jour la liste de la carte dans la base de données
            card_data = self.db.get_card(card_id)
            self.db.update_card(
                card_id,
                card_data['title'],
                card_data['description'],
                len(self.cards),  # Nouvelle position à la fin de la liste
                card_data['due_date'],
                self.list_id  # Nouvelle liste
            )
            
            # Émettre le signal pour informer que la carte a été déplacée
            self.card_moved.emit(card_id, self.list_id)
            
            event.acceptProposedAction()
            
            # Recharger les cartes
            self.load_cards()

    def show_menu(self):
        menu = QMenu(self)
        
        rename_action = menu.addAction("Renommer la liste")
        rename_action.triggered.connect(self.rename_list)
        
        move_action = menu.addAction("Déplacer la liste")
        move_action.triggered.connect(self.move_list)
        
        menu.addSeparator()
        
        delete_action = menu.addAction("Supprimer la liste")
        delete_action.triggered.connect(self.delete_list)
        
        menu.exec_(QCursor.pos())

    def rename_list(self):
        new_title, ok = QInputDialog.getText(
            self, 
            "Renommer la liste",
            "Nouveau nom :",
            QLineEdit.Normal,
            self.title
        )
        if ok and new_title:
            self.title = new_title
            self.db.update_list(self.list_id, new_title, self.get_position())
            # Mettre à jour le titre affiché
            self.findChild(QLabel, "list-title").setText(new_title)

    def move_list(self):
        # Cette méthode sera implémentée plus tard avec un dialogue de sélection de position
        pass

    def delete_list(self):
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment supprimer cette liste ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db.delete_list(self.list_id)
            self.deleteLater()

    def get_position(self):
        # Retourne la position actuelle de la liste
        parent_layout = self.parent().layout()
        return parent_layout.indexOf(self)

