from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
                            QPushButton, QSplitter, QLabel, QFrame)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QIcon
from views.login_view import LoginView
from views.board_list_view import BoardListView
from views.board_view import BoardView
from views.calendar_view import CalendarView
from views.timeline_view import TimelineView
from components.header import Header
from components.sidebar import Sidebar
from components.notification import NotificationPanel
from components.today_projects import TodayProjectsPanel
from components.card_widget import CardDetailDialog

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.user_id = None
        self.username = None
        self.notification_panel_visible = False
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("PyTrello")
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowIcon(QIcon("assets/icons/logo.png"))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.show_boards_requested.connect(self.show_board_list)
        self.sidebar.show_calendar_requested.connect(self.show_calendar)
        self.sidebar.show_timeline_requested.connect(self.show_timeline)
        main_layout.addWidget(self.sidebar)
        
        # Contenu principal
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Header
        self.header = Header(self)
        self.header.logout_requested.connect(self.logout)
        self.header.notification_requested.connect(self.toggle_notification_panel)
        content_layout.addWidget(self.header)
        
        # Zone de contenu principale avec splitter
        self.content_splitter = QSplitter(Qt.Horizontal)
        
        # Zone de contenu principale
        self.stacked_widget = QStackedWidget()
        self.login_view = LoginView(self.db, self.on_login_success)
        self.board_list_view = BoardListView(self.db, self.show_board)
        self.board_view = BoardView(self.db, self.show_board_list)
        self.calendar_view = CalendarView(self.db)
        self.timeline_view = TimelineView(self.db)
        
        self.stacked_widget.addWidget(self.login_view)
        self.stacked_widget.addWidget(self.board_list_view)
        self.stacked_widget.addWidget(self.board_view)
        self.stacked_widget.addWidget(self.calendar_view)
        self.stacked_widget.addWidget(self.timeline_view)
        
        self.content_splitter.addWidget(self.stacked_widget)
        
        # Panneau latéral droit (notifications et projets du jour)
        self.right_panel = QWidget()
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Panneau de notifications
        self.notification_panel = None
        
        # Panneau des projets du jour
        self.today_projects_panel = None
        
        self.content_splitter.addWidget(self.right_panel)
        self.content_splitter.setStretchFactor(0, 3)
        self.content_splitter.setStretchFactor(1, 1)
        
        content_layout.addWidget(self.content_splitter)
        
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)
        
        # Initialiser l'interface
        self.show_login()
        
        # Timer pour les animations
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animations)
        self.animation_timer.start(50)  # 50ms pour des animations fluides
        
    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_view)
        self.header.hide()
        self.sidebar.hide()
        self.right_panel.hide()
        
    def on_login_success(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.header.update_user_info(username)
        self.board_list_view.load_boards(user_id)
        self.stacked_widget.setCurrentWidget(self.board_list_view)
        self.header.show()
        self.sidebar.show()
        self.right_panel.show()
        
        # Initialiser les panneaux latéraux
        self.init_right_panels()
        
    def init_right_panels(self):
        # Nettoyer le layout existant
        while self.right_panel.layout().count():
            item = self.right_panel.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Panneau de notifications
        self.notification_panel = NotificationPanel(self.db, self.user_id)
        self.notification_panel.notification_clicked.connect(self.show_card_from_notification)
        self.notification_panel.load_notifications()
        self.right_panel.layout().addWidget(self.notification_panel)
        
        # Panneau des projets du jour
        self.today_projects_panel = TodayProjectsPanel(self.db, self.user_id)
        self.today_projects_panel.project_clicked.connect(self.show_card_from_project)
        self.today_projects_panel.load_projects()
        self.right_panel.layout().addWidget(self.today_projects_panel)
        
        # Ajouter un espace extensible
        self.right_panel.layout().addStretch()
        
    def show_board(self, board_id, board_title):
        self.board_view.load_board(board_id, board_title)
        self.stacked_widget.setCurrentWidget(self.board_view)
        self.header.set_board_title(board_title)
        
    def show_board_list(self):
        self.board_list_view.load_boards(self.user_id)
        self.stacked_widget.setCurrentWidget(self.board_list_view)
        self.header.clear_board_title()
        
    def show_calendar(self):
        self.calendar_view.load_user_tasks(self.user_id)
        self.stacked_widget.setCurrentWidget(self.calendar_view)
        self.header.set_view_title("Calendrier")
        
    def show_timeline(self):
        self.timeline_view.load_user_tasks(self.user_id)
        self.stacked_widget.setCurrentWidget(self.timeline_view)
        self.header.set_view_title("Chronologie")
        
    def logout(self):
        self.user_id = None
        self.username = None
        self.header.clear_user_info()
        self.show_login()
        
    def toggle_sidebar(self):
        width = self.sidebar.width()
        end_width = 0 if width > 0 else 250
        
        self.animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(end_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()
        
    def toggle_notification_panel(self):
        self.notification_panel_visible = not self.notification_panel_visible
        
        if self.notification_panel_visible:
            self.right_panel.show()
            self.notification_panel.load_notifications()
            self.today_projects_panel.load_projects()
        else:
            self.right_panel.hide()
            
    def show_card_from_notification(self, card_id, notification_type):
        dialog = CardDetailDialog(card_id, self.db)
        if dialog.exec_():
            # Recharger les notifications et projets
            self.notification_panel.load_notifications()
            self.today_projects_panel.load_projects()
            
    def show_card_from_project(self, card_id):
        dialog = CardDetailDialog(card_id, self.db)
        if dialog.exec_():
            # Recharger les notifications et projets
            self.notification_panel.load_notifications()
            self.today_projects_panel.load_projects()
            
    def update_animations(self):
        # Cette méthode est appelée régulièrement pour mettre à jour les animations
        # Vous pouvez ajouter ici des animations supplémentaires si nécessaire
        pass

