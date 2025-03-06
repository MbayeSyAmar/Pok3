from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, 
                            QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon
from datetime import datetime, timedelta

class NotificationPanel(QWidget):
    notification_clicked = pyqtSignal(int, str)  # card_id, notification_type
    
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.notifications = []
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Notifications")
        title.setObjectName("notification-title")
        layout.addWidget(title)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.notifications_layout = QVBoxLayout(self.scroll_content)
        self.notifications_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)
        
        clear_button = QPushButton("Tout effacer")
        clear_button.clicked.connect(self.clear_notifications)
        layout.addWidget(clear_button)
        
        self.setLayout(layout)
        self.setObjectName("notification-panel")
        self.setFixedWidth(300)
        
        # Timer pour vérifier les nouvelles notifications
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_for_notifications)
        self.timer.start(60000)  # Vérifier toutes les minutes
        
    def load_notifications(self):
        self.clear_notifications()
        
        # Récupérer les cartes avec des dates d'échéance proches
        upcoming_tasks = self.get_upcoming_tasks()
        
        for task in upcoming_tasks:
            notification = NotificationItem(
                task['id'],
                f"Rappel: '{task['title']}' est prévu pour {task['due_date']}",
                "reminder",
                task['due_date']
            )
            notification.clicked.connect(self.on_notification_clicked)
            self.notifications.append(notification)
            self.notifications_layout.addWidget(notification)
            
        if not upcoming_tasks:
            no_notifications = QLabel("Aucune notification")
            no_notifications.setAlignment(Qt.AlignCenter)
            self.notifications_layout.addWidget(no_notifications)
            
    def get_upcoming_tasks(self):
        # Récupérer les tâches qui arrivent à échéance dans les 3 prochains jours
        today = datetime.now().date()
        three_days_later = today + timedelta(days=3)
        
        upcoming_tasks = []
        tasks = self.db.get_user_tasks(self.user_id)
        
        for task in tasks:
            due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
            if today <= due_date <= three_days_later:
                upcoming_tasks.append(task)
                
        return upcoming_tasks
        
    def check_for_notifications(self):
        self.load_notifications()
        
    def clear_notifications(self):
        for notification in self.notifications:
            self.notifications_layout.removeWidget(notification)
            notification.deleteLater()
        self.notifications.clear()
        
    def on_notification_clicked(self, card_id, notification_type):
        self.notification_clicked.emit(card_id, notification_type)

class NotificationItem(QWidget):
    clicked = pyqtSignal(int, str)  # card_id, notification_type
    
    def __init__(self, card_id, text, notification_type, time_str):
        super().__init__()
        self.card_id = card_id
        self.notification_type = notification_type
        self.init_ui(text, time_str)
        
    def init_ui(self, text, time_str):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setObjectName("notification-text")
        layout.addWidget(text_label)
        
        time_label = QLabel(time_str)
        time_label.setObjectName("notification-time")
        layout.addWidget(time_label)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        self.setLayout(layout)
        self.setObjectName("notification-item")
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.card_id, self.notification_type)

