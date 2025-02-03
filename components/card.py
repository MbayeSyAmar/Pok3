from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QDialog, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

class Card(QWidget):
    def __init__(self, card_id, title, db):
        super().__init__()
        self.card_id = card_id
        self.title = title
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.title_label = QLabel(self.title)
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label)
        
        edit_button = QPushButton("Éditer")
        edit_button.clicked.connect(self.edit_card)
        layout.addWidget(edit_button)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: white; border-radius: 3px;")
        
    def edit_card(self):
        dialog = CardEditDialog(self.card_id, self.title, self.db)
        if dialog.exec_():
            self.title = dialog.title_input.text()
            self.title_label.setText(self.title)

class CardEditDialog(QDialog):
    def __init__(self, card_id, title, db):
        super().__init__()
        self.card_id = card_id
        self.db = db
        self.init_ui(title)
        
    def init_ui(self, title):
        layout = QVBoxLayout()
        
        self.title_input = QLineEdit(title)
        layout.addWidget(self.title_input)
        
        self.description_input = QTextEdit()
        layout.addWidget(self.description_input)
        
        buttons = QHBoxLayout()
        save_button = QPushButton("Sauvegarder")
        save_button.clicked.connect(self.accept)
        buttons.addWidget(save_button)
        
        cancel_button = QPushButton("Annuler")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(cancel_button)
        
        layout.addLayout(buttons)
        
        self.setLayout(layout)
        
    def accept(self):
        new_title = self.title_input.text()
        new_description = self.description_input.toPlainText()
        self.db.update_card(self.card_id, new_title, new_description, 0, 0)  # Assuming position and list_id don't change
        super().accept()

