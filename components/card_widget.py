from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QDialog, QLineEdit, QTextEdit, QHBoxLayout,
                             QDateEdit, QListWidget, QListWidgetItem, QFileDialog, QScrollArea, QInputDialog, QColorDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QColor

class CardWidget(QWidget):
    card_clicked = pyqtSignal(int)

    def __init__(self, card_id, title, db):
        super().__init__()
        self.card_id = card_id
        self.title = title
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        self.title_label = QLabel(self.title)
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label)
        
        self.setLayout(layout)
        self.setObjectName("card-widget")
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.card_clicked.emit(self.card_id)

class CardDetailDialog(QDialog):
    def __init__(self, card_id, db):
        super().__init__()
        self.card_id = card_id
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        card_data = self.db.get_card(self.card_id)
        
        self.title_input = QLineEdit(card_data['title'])
        scroll_layout.addWidget(QLabel("Titre:"))
        scroll_layout.addWidget(self.title_input)
        
        self.description_input = QTextEdit(card_data['description'])
        scroll_layout.addWidget(QLabel("Description:"))
        scroll_layout.addWidget(self.description_input)
        
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        if card_data['due_date']:
            self.due_date_input.setDate(QDate.fromString(card_data['due_date'], Qt.ISODate))
        else:
            self.due_date_input.setDate(QDate.currentDate())
        scroll_layout.addWidget(QLabel("Date d'échéance:"))
        scroll_layout.addWidget(self.due_date_input)
        
        self.labels_list = QListWidget()
        scroll_layout.addWidget(QLabel("Étiquettes:"))
        scroll_layout.addWidget(self.labels_list)
        self.load_labels()
        
        add_label_button = QPushButton("Ajouter une étiquette")
        add_label_button.clicked.connect(self.add_label)
        scroll_layout.addWidget(add_label_button)
        
        self.checklists = []
        self.load_checklists()
        for checklist in self.checklists:
            scroll_layout.addWidget(checklist)
        
        add_checklist_button = QPushButton("Ajouter une checklist")
        add_checklist_button.clicked.connect(self.add_checklist)
        scroll_layout.addWidget(add_checklist_button)
        
        self.attachments_list = QListWidget()
        scroll_layout.addWidget(QLabel("Pièces jointes:"))
        scroll_layout.addWidget(self.attachments_list)
        self.load_attachments()
        
        add_attachment_button = QPushButton("Ajouter une pièce jointe")
        add_attachment_button.clicked.connect(self.add_attachment)
        scroll_layout.addWidget(add_attachment_button)
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        buttons = QHBoxLayout()
        save_button = QPushButton("Sauvegarder")
        save_button.clicked.connect(self.accept)
        buttons.addWidget(save_button)
        
        cancel_button = QPushButton("Annuler")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(cancel_button)
        
        layout.addLayout(buttons)
        
        self.setLayout(layout)
        self.setWindowTitle(f"Détails de la carte: {card_data['title']}")
        self.resize(400, 600)
        
    def load_labels(self):
        self.labels_list.clear()
        labels = self.db.get_card_labels(self.card_id)
        for label in labels:
            item = QListWidgetItem(label['name'])
            item.setBackground(QColor(label['color']))
            self.labels_list.addItem(item)
        
    def add_label(self):
        board_id = self.db.get_card(self.card_id)['list_id']  # Assuming list_id is actually board_id
        label_dialog = LabelDialog(self.db, board_id)
        if label_dialog.exec_():
            label_id = label_dialog.selected_label_id
            self.db.add_label_to_card(self.card_id, label_id)
            self.load_labels()
        
    def load_checklists(self):
        checklists = self.db.get_checklists(self.card_id)
        for checklist in checklists:
            checklist_widget = ChecklistWidget(checklist['id'], checklist['title'], self.db)
            self.checklists.append(checklist_widget)
        
    def add_checklist(self):
        title, ok = QInputDialog.getText(self, "Nouvelle checklist", "Titre de la checklist:")
        if ok and title:
            checklist_id = self.db.create_checklist(title, self.card_id)
            checklist_widget = ChecklistWidget(checklist_id, title, self.db)
            self.checklists.append(checklist_widget)
            self.layout().insertWidget(self.layout().count() - 1, checklist_widget)
        
    def load_attachments(self):
        self.attachments_list.clear()
        attachments = self.db.get_attachments(self.card_id)
        for attachment in attachments:
            self.attachments_list.addItem(attachment['filename'])
        
    def add_attachment(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier")
        if file_path:
            filename = file_path.split('/')[-1]
            self.db.create_attachment(filename, file_path, self.card_id)
            self.load_attachments()
        
    def accept(self):
        new_title = self.title_input.text()
        new_description = self.description_input.toPlainText()
        new_due_date = self.due_date_input.date().toString(Qt.ISODate)
        self.db.update_card(self.card_id, new_title, new_description, 0, new_due_date, 0)  # Assuming position and list_id don't change
        super().accept()

class LabelDialog(QDialog):
    def __init__(self, db, board_id):
        super().__init__()
        self.db = db
        self.board_id = board_id
        self.selected_label_id = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.labels_list = QListWidget()
        self.load_labels()
        layout.addWidget(self.labels_list)
        
        add_label_button = QPushButton("Nouvelle étiquette")
        add_label_button.clicked.connect(self.add_new_label)
        layout.addWidget(add_label_button)
        
        buttons = QHBoxLayout()
        select_button = QPushButton("Sélectionner")
        select_button.clicked.connect(self.select_label)
        buttons.addWidget(select_button)
        
        cancel_button = QPushButton("Annuler")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(cancel_button)
        
        layout.addLayout(buttons)
        
        self.setLayout(layout)
        self.setWindowTitle("Sélectionner une étiquette")
        
    def load_labels(self):
        self.labels_list.clear()
        labels = self.db.get_labels(self.board_id)
        for label in labels:
            item = QListWidgetItem(label['name'])
            item.setBackground(QColor(label['color']))
            item.setData(Qt.UserRole, label['id'])
            self.labels_list.addItem(item)
        
    def add_new_label(self):
        name, ok = QInputDialog.getText(self, "Nouvelle étiquette", "Nom de l'étiquette:")
        if ok and name:
            color = QColorDialog.getColor()
            if color.isValid():
                self.db.create_label(name, color.name(), self.board_id)
                self.load_labels()
        
    def select_label(self):
        selected_items = self.labels_list.selectedItems()
        if selected_items:
            self.selected_label_id = selected_items[0].data(Qt.UserRole)
            self.accept()

class ChecklistWidget(QWidget):
    def __init__(self, checklist_id, title, db):
        super().__init__()
        self.checklist_id = checklist_id
        self.title = title
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        title_layout = QHBoxLayout()
        self.title_label = QLabel(self.title)
        title_layout.addWidget(self.title_label)
        
        add_item_button = QPushButton("+")
        add_item_button.clicked.connect(self.add_item)
        title_layout.addWidget(add_item_button)
        
        layout.addLayout(title_layout)
        
        self.items_list = QListWidget()
        self.load_items()
        layout.addWidget(self.items_list)
        
        self.setLayout(layout)
        
    def load_items(self):
        self.items_list.clear()
        items = self.db.get_checklist_items(self.checklist_id)
        for item in items:
            list_item = QListWidgetItem(item['content'])
            list_item.setCheckState(Qt.Checked if item['is_checked'] else Qt.Unchecked)
            list_item.setData(Qt.UserRole, item['id'])
            self.items_list.addItem(list_item)
        
    def add_item(self):
        content, ok = QInputDialog.getText(self, "Nouvel élément", "Contenu de l'élément:")
        if ok and content:
            position = self.items_list.count()
            self.db.create_checklist_item(content, position, self.checklist_id)
            self.load_items()

