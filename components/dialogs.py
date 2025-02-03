from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.user_id = None
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur de la boîte de dialogue de connexion."""
        layout = QVBoxLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        login_button = QPushButton("Se connecter")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)
        
        register_button = QPushButton("S'inscrire")
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)
        
        self.setLayout(layout)
        
    def login(self):
        """Gère la connexion de l'utilisateur."""
        username = self.username_input.text()
        password = self.password_input.text()
        
        user = self.db.get_user(username)
        if user and user['password'] == password:
            self.user_id = user['id']
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
        
    def register(self):
        """Gère l'inscription d'un nouvel utilisateur."""
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return
        
        existing_user = self.db.get_user(username)
        if existing_user:
            QMessageBox.warning(self, "Erreur", "Ce nom d'utilisateur est déjà pris.")
            return
        
        self.db.create_user(username, password)
        QMessageBox.information(self, "Succès", "Inscription réussie. Vous pouvez maintenant vous connecter.")

class CreateBoardDialog(QDialog):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur de la boîte de dialogue de création de tableau."""
        layout = QVBoxLayout()
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Titre du tableau")
        layout.addWidget(self.title_input)
        
        create_button = QPushButton("Créer")
        create_button.clicked.connect(self.create_board)
        layout.addWidget(create_button)
        
        self.setLayout(layout)
        
    def create_board(self):
        """Crée un nouveau tableau."""
        title = self.title_input.text()
        
        if not title:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un titre pour le tableau.")
            return
        
        self.db.create_board(title, self.user_id)
        self.accept()

