from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QInputDialog, QHBoxLayout
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from components.card_widget import CardDetailDialog

class TimelineView(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.user_id = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        add_task_button = QPushButton("Ajouter une tâche")
        add_task_button.clicked.connect(self.add_task)
        layout.addWidget(add_task_button)

        self.setLayout(layout)

    def load_user_tasks(self, user_id):
        self.user_id = user_id
        self.user_tasks = self.db.get_user_tasks(user_id)
        self.update_timeline()

    def update_timeline(self):
        # Supprimer les widgets existants dans le layout
        for i in reversed(range(self.scroll_layout.count())):
            item = self.scroll_layout.itemAt(i)
            widget = item.widget()
            if widget:  # Vérifie si l'élément est un widget
                widget.setParent(None)

        # Si aucune tâche n'est trouvée
        if not self.user_tasks:
            self.scroll_layout.addWidget(QLabel("Aucune tâche trouvée"))
            return

        # Calculer les dates minimales et maximales
        min_date = min(QDate.fromString(task['due_date'], Qt.ISODate) for task in self.user_tasks)
        max_date = max(QDate.fromString(task['due_date'], Qt.ISODate) for task in self.user_tasks)

        current_date = min_date
        while current_date <= max_date:
            # Ajouter une étiquette pour la date
            date_label = QLabel(current_date.toString("dd MMMM yyyy"))
            date_label.setStyleSheet("font-weight: bold;")
            self.scroll_layout.addWidget(date_label)

            # Ajouter les tâches correspondant à cette date
            for task in self.user_tasks:
                task_date = QDate.fromString(task['due_date'], Qt.ISODate)
                if task_date == current_date:
                    task_widget = TaskWidget(task, self.db)
                    task_widget.task_updated.connect(self.load_user_tasks)
                    self.scroll_layout.addWidget(task_widget)

            # Passer au jour suivant
            current_date = current_date.addDays(1)

        # Ajouter un espace pour remplir le layout
        self.scroll_layout.addStretch()


    def add_task(self):
        title, ok = QInputDialog.getText(self, "Nouvelle tâche", "Titre de la tâche:")
        if ok and title:
            due_date, ok = QInputDialog.getText(self, "Date d'échéance", "Date d'échéance (YYYY-MM-DD):")
            if ok and due_date:
                # Assuming the task is added to the first list of the first board
                boards = self.db.get_boards(self.user_id)
                if boards:
                    lists = self.db.get_lists(boards[0]['id'])
                    if lists:
                        new_card_id = self.db.create_card(title, "", 0, due_date, lists[0]['id'])
                        self.load_user_tasks(self.user_id)

class TaskWidget(QWidget):
    task_updated = pyqtSignal(int)

    def __init__(self, task, db):
        super().__init__()
        self.task = task
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(f"Titre: {self.task['title']}"))
        layout.addWidget(QLabel(f"Tableau: {self.task['board_title']}"))
        layout.addWidget(QLabel(f"Liste: {self.task['list_title']}"))

        edit_button = QPushButton("Éditer")
        edit_button.clicked.connect(self.edit_task)
        layout.addWidget(edit_button)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #f0f0f0; border-radius: 5px; padding: 5px;")

    def edit_task(self):
        dialog = CardDetailDialog(self.task['id'], self.db)
        if dialog.exec_():
            self.task_updated.emit(self.task['id'])

