from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from utils.styles import apply_dark_theme

class SettingsView(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur de la vue des paramètres."""
        layout = QVBoxLayout()
        
        # Sélection du thème
        theme_label = QLabel("Thème :")
        layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Clair", "Sombre"])
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        layout.addWidget(self.theme_combo)
        
        # Bouton de sauvegarde
        save_button = QPushButton("Sauvegarder")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        
        self.setLayout(layout)
        
    def change_theme(self, index):
        """Change le thème de l'application."""
        if index == 1:  # Thème sombre
            apply_dark_theme(self.window())
        else:  # Thème clair
            # Implémentez ici la logique pour appliquer le thème clair
            pass
        
    def save_settings(self):
        """Sauvegarde les paramètres de l'application."""
        # Implémentez ici la logique pour sauvegarder les paramètres
        pass

