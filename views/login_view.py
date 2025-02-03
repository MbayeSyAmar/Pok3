from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class LoginView(QWidget):
    login_success = pyqtSignal(int, str)

    def __init__(self, db, on_login_success):
        super().__init__()
        self.db = db
        self.on_login_success = on_login_success
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("assets/images/logo.png")
        logo.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(logo, alignment=Qt.AlignCenter)

        title = QLabel("Bienvenue sur PyTache")
        title.setObjectName("login-title")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        button_layout = QHBoxLayout()
        login_button = QPushButton("Se connecter")
        login_button.clicked.connect(self.login)
        button_layout.addWidget(login_button)

        register_button = QPushButton("S'inscrire")
        register_button.clicked.connect(self.register)
        button_layout.addWidget(register_button)

        layout.addLayout(button_layout)

        self.message_label = QLabel()
        self.message_label.setObjectName("message-label")
        layout.addWidget(self.message_label)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user = self.db.get_user(username)
        if user and user['password'] == password:
            self.on_login_success(user['id'], user['username'])
        else:
            self.show_error("Nom d'utilisateur ou mot de passe incorrect.")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()

        if not username or not password or not email:
            self.show_error("Veuillez remplir tous les champs.")
            return

        existing_user = self.db.get_user(username)
        if existing_user:
            self.show_error("Ce nom d'utilisateur est déjà pris.")
            return

        user_id = self.db.create_user(username, password, email)
        self.show_success("Inscription réussie. Vous pouvez maintenant vous connecter.")
        self.on_login_success(user_id, username)

    def show_error(self, message):
        self.message_label.setText(message)
        self.message_label.setStyleSheet("color: red;")

    def show_success(self, message):
        self.message_label.setText(message)
        self.message_label.setStyleSheet("color: green;")

