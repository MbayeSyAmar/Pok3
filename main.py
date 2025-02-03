import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont
from main_window import MainWindow
from database import Database
from utils.styles import load_stylesheet

def main():
    app = QApplication(sys.argv)
    
    # Charger la police Roboto
    font_id = QFontDatabase.addApplicationFont("assets/fonts/Roboto-Regular.ttf")
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family, 10))
    
    db = Database()
    db.create_tables()
    
    stylesheet = load_stylesheet("assets/styles/main.qss")
    app.setStyleSheet(stylesheet)
    
    main_window = MainWindow(db)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

