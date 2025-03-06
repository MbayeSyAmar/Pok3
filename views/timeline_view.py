from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QLabel, 
                           QPushButton, QInputDialog, QHBoxLayout)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from components.card_widget import CardDetailDialog

class TimelineView(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.user_id = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Titre
        title = QLabel("Chronologie")
        title.setObjectName("page-title")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)

        # Zone de défilement
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setSpacing(16)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # Bouton d'ajout
        add_task_button = QPushButton("+ Ajouter une tâche")
        add_task_button.setObjectName("add-task-button")
        add_task_button.clicked.connect(self.add_task)
        layout.addWidget(add_task_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def load_user_tasks(self, user_id):
        self.user_id = user_id
        self.user_tasks = self.db.get_user_tasks(user_id)
        self.update_timeline()

    def update_timeline(self):
        # Nettoyer la vue
        for i in reversed(range(self.scroll_layout.count())): 
            self.scroll_layout.itemAt(i).widget().setParent(None)

        if not self.user_tasks:
            no_tasks = QLabel("Aucune tâche planifiée")
            no_tasks.setAlignment(Qt.AlignCenter)
            no_tasks.setStyleSheet("color: #B3B3B3; font-size: 16px;")
            self.scroll_layout.addWidget(no_tasks)
            return

        # Grouper les tâches par date
        tasks_by_date = {}
        for task in self.user_tasks:
            if task['due_date']:  # Ne traiter que les tâches avec une date
                date = QDate.fromString(task['due_date'], Qt.ISODate)
                if date not in tasks_by_date:
                    tasks_by_date[date] = []
                tasks_by_date[date].append(task)

        # Afficher les tâches groupées par date
        for date in sorted(tasks_by_date.keys()):
            # En-tête de date
            date_widget = QWidget()
            date_layout = QVBoxLayout(date_widget)
            date_layout.setContentsMargins(0, 0, 0, 16)

            date_header = QLabel(date.toString("dd MMMM yyyy"))
            date_header.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #7C4DFF;
                padding: 8px;
                background-color: #2D2D2D;
                border-radius: 4px;
            """)
            date_layout.addWidget(date_header)

            # Tâches de la journée
            for task in tasks_by_date[date]:
                task_widget = TaskWidget(task, self.db)
                task_widget.task_updated.connect(lambda: self.load_user_tasks(self.user_id))
                date_layout.addWidget(task_widget)

            self.scroll_layout.addWidget(date_widget)

    def add_task(self):
        title, ok = QInputDialog.getText(self, "Nouvelle tâche", "Titre de la tâche:")
        if ok and title:
            due_date, ok = QInputDialog.getText(self, "Date d'échéance", "Date d'échéance (YYYY-MM-DD):")
            if ok and due_date:
                boards = self.db.get_boards(self.user_id)
                if boards:
                    lists = self.db.get_lists(boards[0]['id'])
                    if lists:
                        self.db.create_card(title, "", 0, due_date, lists[0]['id'])
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
        layout.setContentsMargins(8, 8, 8, 8)

        # Informations de la tâche
        info_layout = QVBoxLayout()
        
        title = QLabel(self.task['title'])
        title.setStyleSheet("font-weight: bold; font-size: 16px; color: #FFFFFF;")
        info_layout.addWidget(title)

        details = QLabel(f"{self.task['board_title']} • {self.task['list_title']}")
        details.setStyleSheet("color: #B3B3B3; font-size: 12px;")
        info_layout.addWidget(details)

        layout.addLayout(info_layout)
        layout.addStretch()

        # Boutons d'action
        edit_button = QPushButton("Éditer")
        edit_button.setObjectName("task-action-button")
        edit_button.clicked.connect(self.edit_task)
        layout.addWidget(edit_button)

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #2D2D2D;
                border-radius: 6px;
            }
            #task-action-button {
                background-color: #7C4DFF;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: 500;
            }
            #task-action-button:hover {
                background-color: #9575FF;
            }
        """)

    def edit_task(self):
        dialog = CardDetailDialog(self.task['id'], self.db)
        if dialog.exec_():
            self.task_updated.emit(self.task['id'])

