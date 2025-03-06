from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from datetime import datetime

class TodayProjectsPanel(QWidget):
    project_clicked = pyqtSignal(int)  # card_id
    
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.projects = []
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("Projets du jour")
        title.setObjectName("today-projects-title")
        layout.addWidget(title)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.projects_layout = QVBoxLayout(self.scroll_content)
        self.projects_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)
        
        self.setLayout(layout)
        self.setObjectName("today-projects-panel")
        
    def load_projects(self):
        self.clear_projects()
        
        # Récupérer les cartes avec des dates d'échéance aujourd'hui
        today_tasks = self.get_today_tasks()
        
        for task in today_tasks:
            project = ProjectItem(
                task['id'],
                task['title'],
                task['board_title'],
                task['list_title'],
                task['due_date']
            )
            project.clicked.connect(self.project_clicked.emit)
            self.projects.append(project)
            self.projects_layout.addWidget(project)
            
        if not today_tasks:
            no_projects = QLabel("Aucun projet prévu aujourd'hui")
            no_projects.setAlignment(Qt.AlignCenter)
            self.projects_layout.addWidget(no_projects)
            
    def get_today_tasks(self):
        # Récupérer les tâches qui arrivent à échéance aujourd'hui
        today = datetime.now().date().isoformat()
        
        today_tasks = []
        tasks = self.db.get_user_tasks(self.user_id)
        
        for task in tasks:
            if task['due_date'] == today:
                today_tasks.append(task)
                
        return today_tasks
        
    def clear_projects(self):
        for project in self.projects:
            self.projects_layout.removeWidget(project)
            project.deleteLater()
        self.projects.clear()

class ProjectItem(QWidget):
    clicked = pyqtSignal(int)  # card_id
    
    def __init__(self, card_id, title, board_title, list_title, due_date):
        super().__init__()
        self.card_id = card_id
        self.init_ui(title, board_title, list_title, due_date)
        
    def init_ui(self, title, board_title, list_title, due_date):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        title_label = QLabel(title)
        title_label.setWordWrap(True)
        title_label.setObjectName("today-project-title")
        layout.addWidget(title_label)
        
        info_layout = QHBoxLayout()
        board_label = QLabel(f"Tableau: {board_title}")
        info_layout.addWidget(board_label)
        
        list_label = QLabel(f"Liste: {list_title}")
        info_layout.addWidget(list_label)
        layout.addLayout(info_layout)
        
        due_label = QLabel(f"Échéance: {due_date}")
        due_label.setObjectName("today-project-due")
        layout.addWidget(due_label)
        
        self.setLayout(layout)
        self.setObjectName("today-project-item")
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.card_id)

