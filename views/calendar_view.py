from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QListWidget, QListWidgetItem, QPushButton, QInputDialog
from PyQt5.QtCore import QDate, Qt
from components.card_widget import CardDetailDialog

class CalendarView(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.user_id = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.update_task_list)
        layout.addWidget(self.calendar)

        self.task_list = QListWidget()
        self.task_list.itemDoubleClicked.connect(self.show_task_details)
        layout.addWidget(self.task_list)

        add_task_button = QPushButton("Ajouter une tâche")
        add_task_button.clicked.connect(self.add_task)
        layout.addWidget(add_task_button)

        self.setLayout(layout)

    def load_user_tasks(self, user_id):
        self.user_id = user_id
        self.user_tasks = self.db.get_user_tasks(user_id)
        self.update_task_list()

    def update_task_list(self):
        self.task_list.clear()
        selected_date = self.calendar.selectedDate()
        
        for task in self.user_tasks:
            task_date = QDate.fromString(task['due_date'], Qt.ISODate)
            if task_date == selected_date:
                item = QListWidgetItem(f"{task['title']} - {task['board_title']} - {task['list_title']}")
                item.setData(Qt.UserRole, task['id'])
                self.task_list.addItem(item)

    def show_task_details(self, item):
        card_id = item.data(Qt.UserRole)
        dialog = CardDetailDialog(card_id, self.db)
        if dialog.exec_():
            self.load_user_tasks(self.user_id)  # Reload tasks to reflect any changes

    def add_task(self):
        title, ok = QInputDialog.getText(self, "Nouvelle tâche", "Titre de la tâche:")
        if ok and title:
            due_date = self.calendar.selectedDate().toString(Qt.ISODate)
            # Assuming the task is added to the first list of the first board
            boards = self.db.get_boards(self.user_id)
            if boards:
                lists = self.db.get_lists(boards[0]['id'])
                if lists:
                    new_card_id = self.db.create_card(title, "", 0, due_date, lists[0]['id'])
                    self.load_user_tasks(self.user_id)
                    self.update_task_list()

