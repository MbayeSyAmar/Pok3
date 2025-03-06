from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QDialog, QLineEdit, QTextEdit, QHBoxLayout,
                             QDateEdit, QListWidget, QListWidgetItem, QFileDialog, QScrollArea, QColorDialog, QInputDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QMimeData, QPoint
from PyQt5.QtGui import QColor, QDrag, QPixmap, QPainter

class CardWidget(QWidget):
    card_clicked = pyqtSignal(int)
    card_moved = pyqtSignal(int, int)  # card_id, new_list_id

    def __init__(self, card_id, title, db):
        super().__init__()
        self.card_id = card_id
        self.title = title
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Labels container
        labels_layout = QHBoxLayout()
        labels_layout.setSpacing(4)
        labels = self.db.get_card_labels(self.card_id)
        
        for label in labels:
            label_widget = QLabel()
            label_widget.setFixedHeight(6)
            label_widget.setMinimumWidth(40)
            label_widget.setStyleSheet(f"""
                background-color: {label['color']};
                border-radius: 3px;
            """)
            labels_layout.addWidget(label_widget)
        
        labels_layout.addStretch()
        layout.addLayout(labels_layout)
        
        # Titre
        self.title_label = QLabel(self.title)
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("""
            color: #FFFFFF;
            font-size: 14px;
            font-weight: 500;
        """)
        layout.addWidget(self.title_label)
        
        # Informations supplémentaires
        info_layout = QHBoxLayout()
        info_layout.setSpacing(8)
        
        # Date d'échéance
        card_data = self.db.get_card(self.card_id)
        if card_data and card_data['due_date']:
            due_date = QLabel(f"📅 {card_data['due_date']}")
            due_date.setStyleSheet("""
                color: #FF80AB;
                font-size: 12px;
            """)
            info_layout.addWidget(due_date)
        
        # Checklist progress
        checklists = self.db.get_checklists(self.card_id)
        if checklists:
            total_items = 0
            checked_items = 0
            for checklist in checklists:
                items = self.db.get_checklist_items(checklist['id'])
                total_items += len(items)
                checked_items += len([item for item in items if item['is_checked']])
            
            if total_items > 0:
                progress = QLabel(f"✓ {checked_items}/{total_items}")
                progress.setStyleSheet("""
                    color: #B3B3B3;
                    font-size: 12px;
                """)
                info_layout.addWidget(progress)
        
        # Attachments indicator
        attachments = self.db.get_attachments(self.card_id)
        if attachments:
            attach_label = QLabel(f"📎 {len(attachments)}")
            attach_label.setStyleSheet("""
                color: #B3B3B3;
                font-size: 12px;
            """)
            info_layout.addWidget(attach_label)
        
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        self.setLayout(layout)
        self.setObjectName("card-widget")
        self.setCursor(Qt.PointingHandCursor)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.card_clicked.emit(self.card_id)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
            
        if (event.pos() - self.drag_start_position).manhattanLength() < 10:
            return
            
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(str(self.card_id))
        drag.setMimeData(mime_data)
        
        # Créer une image de la carte pour le drag
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        self.render(painter)
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        
        # Commencer le drag
        drag.exec_(Qt.MoveAction)
        
    def mouseReleaseEvent(self, event):
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
        
        # Titre
        title_label = QLabel("Titre")
        title_label.setObjectName("card-detail-section-title")
        scroll_layout.addWidget(title_label)
        
        self.title_input = QLineEdit(card_data['title'])
        self.title_input.setObjectName("card-detail-title")
        scroll_layout.addWidget(self.title_input)
        
        # Description
        desc_label = QLabel("Description")
        desc_label.setObjectName("card-detail-section-title")
        scroll_layout.addWidget(desc_label)
        
        self.description_input = QTextEdit(card_data['description'] if card_data['description'] else "")
        scroll_layout.addWidget(self.description_input)
        
        # Date d'échéance
        due_label = QLabel("Date d'échéance")
        due_label.setObjectName("card-detail-section-title")
        scroll_layout.addWidget(due_label)
        
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        if card_data['due_date']:
            self.due_date_input.setDate(QDate.fromString(card_data['due_date'], Qt.ISODate))
        else:
            self.due_date_input.setDate(QDate.currentDate())
        scroll_layout.addWidget(self.due_date_input)
        
        # Étiquettes
        labels_label = QLabel("Étiquettes")
        labels_label.setObjectName("card-detail-section-title")
        scroll_layout.addWidget(labels_label)
        
        self.labels_list = QListWidget()
        self.labels_list.setMaximumHeight(100)
        scroll_layout.addWidget(self.labels_list)
        self.load_labels()
        
        labels_buttons = QHBoxLayout()
        add_label_button = QPushButton("Ajouter")
        add_label_button.clicked.connect(self.add_label)
        labels_buttons.addWidget(add_label_button)
        
        remove_label_button = QPushButton("Supprimer")
        remove_label_button.clicked.connect(self.remove_label)
        labels_buttons.addWidget(remove_label_button)
        
        scroll_layout.addLayout(labels_buttons)
        
        # Checklists
        checklists_label = QLabel("Checklists")
        checklists_label.setObjectName("card-detail-section-title")
        scroll_layout.addWidget(checklists_label)
        
        self.checklists_layout = QVBoxLayout()
        scroll_layout.addLayout(self.checklists_layout)
        
        self.checklists = []
        self.load_checklists()
        
        add_checklist_button = QPushButton("Ajouter une checklist")
        add_checklist_button.clicked.connect(self.add_checklist)
        scroll_layout.addWidget(add_checklist_button)
        
        # Pièces jointes
        attachments_label = QLabel("Pièces jointes")
        attachments_label.setObjectName("card-detail-section-title")
        scroll_layout.addWidget(attachments_label)
        
        self.attachments_list = QListWidget()
        self.attachments_list.setMaximumHeight(100)
        scroll_layout.addWidget(self.attachments_list)
        self.load_attachments()
        
        attachments_buttons = QHBoxLayout()
        add_attachment_button = QPushButton("Ajouter")
        add_attachment_button.clicked.connect(self.add_attachment)
        attachments_buttons.addWidget(add_attachment_button)
        
        remove_attachment_button = QPushButton("Supprimer")
        remove_attachment_button.clicked.connect(self.remove_attachment)
        attachments_buttons.addWidget(remove_attachment_button)
        
        scroll_layout.addLayout(attachments_buttons)
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        # Boutons de sauvegarde/annulation
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
        self.setObjectName("card-detail-dialog")
        self.resize(500, 700)
        
    def load_labels(self):
        self.labels_list.clear()
        labels = self.db.get_card_labels(self.card_id)
        for label in labels:
            item = QListWidgetItem(label['name'])
            item.setBackground(QColor(label['color']))
            item.setForeground(QColor("white"))
            item.setData(Qt.UserRole, label['id'])
            self.labels_list.addItem(item)
        
    def add_label(self):
        board_id = 1  # Remplacer par la vraie board_id
        name, ok = QInputDialog.getText(self, "Nouvelle étiquette", "Nom de l'étiquette:")
        if ok and name:
            color = QColorDialog.getColor()
            if color.isValid():
                label_id = self.db.create_label(name, color.name(), board_id)
                self.db.add_label_to_card(self.card_id, label_id)
                self.load_labels()
        
    def remove_label(self):
        selected_items = self.labels_list.selectedItems()
        if selected_items:
            label_id = selected_items[0].data(Qt.UserRole)
            self.db.remove_label_from_card(self.card_id, label_id)
            self.load_labels()
        
    def load_checklists(self):
        checklists = self.db.get_checklists(self.card_id)
        for checklist in checklists:
            checklist_widget = ChecklistWidget(checklist['id'], checklist['title'], self.db)
            self.checklists.append(checklist_widget)
            self.checklists_layout.addWidget(checklist_widget)
        
    def add_checklist(self):
        title, ok = QInputDialog.getText(self, "Nouvelle checklist", "Titre de la checklist:")
        if ok and title:
            checklist_id = self.db.create_checklist(title, self.card_id)
            checklist_widget = ChecklistWidget(checklist_id, title, self.db)
            self.checklists.append(checklist_widget)
            self.checklists_layout.addWidget(checklist_widget)
        
    def load_attachments(self):
        self.attachments_list.clear()
        attachments = self.db.get_attachments(self.card_id)
        for attachment in attachments:
            item = QListWidgetItem(attachment['filename'])
            item.setData(Qt.UserRole, attachment['id'])
            self.attachments_list.addItem(item)
        
    def add_attachment(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier")
        if file_path:
            filename = file_path.split('/')[-1]
            self.db.create_attachment(filename, file_path, self.card_id)
            self.load_attachments()
            
    def remove_attachment(self):
        selected_items = self.attachments_list.selectedItems()
        if selected_items:
            attachment_id = selected_items[0].data(Qt.UserRole)
            self.db.delete_attachment(attachment_id)
            self.load_attachments()
        
    def accept(self):
        new_title = self.title_input.text()
        new_description = self.description_input.toPlainText()
        new_due_date = self.due_date_input.date().toString(Qt.ISODate)
        
        # Récupérer les données actuelles de la carte
        card_data = self.db.get_card(self.card_id)
        
        self.db.update_card(
            self.card_id, 
            new_title, 
            new_description, 
            card_data['position'], 
            new_due_date, 
            card_data['list_id']
        )
        super().accept()

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
        self.title_label.setObjectName("card-detail-section-title")
        title_layout.addWidget(self.title_label)
        
        add_item_button = QPushButton("+")
        add_item_button.setFixedWidth(30)
        add_item_button.clicked.connect(self.add_item)
        title_layout.addWidget(add_item_button)
        
        layout.addLayout(title_layout)
        
        self.items_list = QListWidget()
        self.items_list.setMaximumHeight(150)
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
        
        self.items_list.itemChanged.connect(self.item_checked_changed)
        
    def add_item(self):
        content, ok = QInputDialog.getText(self, "Nouvel élément", "Contenu de l'élément:")
        if ok and content:
            position = self.items_list.count()
            self.db.create_checklist_item(content, position, self.checklist_id)
            self.load_items()
            
    def item_checked_changed(self, item):
        item_id = item.data(Qt.UserRole)
        is_checked = item.checkState() == Qt.Checked
        
        # Mettre à jour l'état de l'élément dans la base de données
        self.db.update_checklist_item(item_id, item.text(), is_checked, 0)  # 0 est la position par défaut

