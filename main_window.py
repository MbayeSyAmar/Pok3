from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon
from views.login_view import LoginView
from views.board_list_view import BoardListView
from views.board_view import BoardView
from views.calendar_view import CalendarView
from views.timeline_view import TimelineView
from components.header import Header
from components.sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.user_id = None
        self.username = None
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
        
        self.sidebar = Sidebar(self)
        self.sidebar.show_boards_requested.connect(self.show_board_list)
        self.sidebar.show_calendar_requested.connect(self.show_calendar)
        self.sidebar.show_timeline_requested.connect(self.show_timeline)
        main_layout.addWidget(self.sidebar)
        
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        self.header = Header(self)
        self.header.logout_requested.connect(self.logout)
        content_layout.addWidget(self.header)
        
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
        
        content_layout.addWidget(self.stacked_widget)
        
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)
        
        self.show_login()
        
    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_view)
        self.header.hide()
        self.sidebar.hide()
        
    def on_login_success(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.header.update_user_info(username)
        self.board_list_view.load_boards(user_id)
        self.stacked_widget.setCurrentWidget(self.board_list_view)
        self.header.show()
        self.sidebar.show()
        
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

