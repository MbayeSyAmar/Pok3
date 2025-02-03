import sqlite3
from PyQt5.QtCore import QObject, pyqtSignal
from datetime import datetime

class Database(QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('pytrello.db')
        self.conn.row_factory = sqlite3.Row

    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS boards (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            background TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lists (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            position INTEGER,
            board_id INTEGER,
            FOREIGN KEY (board_id) REFERENCES boards (id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            position INTEGER,
            due_date TEXT,
            list_id INTEGER,
            FOREIGN KEY (list_id) REFERENCES lists (id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS labels (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            color TEXT NOT NULL,
            board_id INTEGER,
            FOREIGN KEY (board_id) REFERENCES boards (id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS card_labels (
            card_id INTEGER,
            label_id INTEGER,
            FOREIGN KEY (card_id) REFERENCES cards (id),
            FOREIGN KEY (label_id) REFERENCES labels (id),
            PRIMARY KEY (card_id, label_id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS checklists (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            card_id INTEGER,
            FOREIGN KEY (card_id) REFERENCES cards (id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS checklist_items (
            id INTEGER PRIMARY KEY,
            content TEXT NOT NULL,
            is_checked BOOLEAN,
            position INTEGER,
            checklist_id INTEGER,
            FOREIGN KEY (checklist_id) REFERENCES checklists (id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS attachments (
            id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            uploaded_at TEXT NOT NULL,
            card_id INTEGER,
            FOREIGN KEY (card_id) REFERENCES cards (id)
        )
        ''')
        
        self.conn.commit()

    def execute_query(self, query, params=None):
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.conn.commit()
        return cursor

    # User methods
    def create_user(self, username, password, email):
        query = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
        self.execute_query(query, (username, password, email))
        self.data_changed.emit()
        return self.execute_query("SELECT last_insert_rowid()").fetchone()[0]

    def get_user(self, username):
        query = "SELECT * FROM users WHERE username = ?"
        return self.execute_query(query, (username,)).fetchone()

    # Board methods
    def create_board(self, title, background, user_id):
        query = "INSERT INTO boards (title, background, user_id) VALUES (?, ?, ?)"
        self.execute_query(query, (title, background, user_id))
        self.data_changed.emit()
        return self.execute_query("SELECT last_insert_rowid()").fetchone()[0]

    def get_boards(self, user_id):
        query = "SELECT * FROM boards WHERE user_id = ?"
        return self.execute_query(query, (user_id,)).fetchall()

    def update_board(self, board_id, title, background):
        query = "UPDATE boards SET title = ?, background = ? WHERE id = ?"
        self.execute_query(query, (title, background, board_id))
        self.data_changed.emit()

    def delete_board(self, board_id):
        queries = [
            "DELETE FROM card_labels WHERE card_id IN (SELECT id FROM cards WHERE list_id IN (SELECT id FROM lists WHERE board_id = ?))",
            "DELETE FROM checklist_items WHERE checklist_id IN (SELECT id FROM checklists WHERE card_id IN (SELECT id FROM cards WHERE list_id IN (SELECT id FROM lists WHERE board_id = ?)))",
            "DELETE FROM checklists WHERE card_id IN (SELECT id FROM cards WHERE list_id IN (SELECT id FROM lists WHERE board_id = ?))",
            "DELETE FROM attachments WHERE card_id IN (SELECT id FROM cards WHERE list_id IN (SELECT id FROM lists WHERE board_id = ?))",
            "DELETE FROM cards WHERE list_id IN (SELECT id FROM lists WHERE board_id = ?)",
            "DELETE FROM lists WHERE board_id = ?",
            "DELETE FROM labels WHERE board_id = ?",
            "DELETE FROM boards WHERE id = ?"
        ]
        for query in queries:
            self.execute_query(query, (board_id,))
        self.data_changed.emit()

    # List methods
    def create_list(self, title, position, board_id):
        query = "INSERT INTO lists (title, position, board_id) VALUES (?, ?, ?)"
        self.execute_query(query, (title, position, board_id))
        self.data_changed.emit()
        return self.execute_query("SELECT last_insert_rowid()").fetchone()[0]

    def get_lists(self, board_id):
        query = "SELECT * FROM lists WHERE board_id = ? ORDER BY position"
        return self.execute_query(query, (board_id,)).fetchall()

    def update_list(self, list_id, title, position):
        query = "UPDATE lists SET title = ?, position = ? WHERE id = ?"
        self.execute_query(query, (title, position, list_id))
        self.data_changed.emit()

    def delete_list(self, list_id):
        queries = [
            "DELETE FROM card_labels WHERE card_id IN (SELECT id FROM cards WHERE list_id = ?)",
            "DELETE FROM checklist_items WHERE checklist_id IN (SELECT id FROM checklists WHERE card_id IN (SELECT id FROM cards WHERE list_id = ?))",
            "DELETE FROM checklists WHERE card_id IN (SELECT id FROM cards WHERE list_id = ?)",
            "DELETE FROM attachments WHERE card_id IN (SELECT id FROM cards WHERE list_id = ?)",
            "DELETE FROM cards WHERE list_id = ?",
            "DELETE FROM lists WHERE id = ?"
        ]
        for query in queries:
            self.execute_query(query, (list_id,))
        self.data_changed.emit()

    # Card methods
    def create_card(self, title, description, position, due_date, list_id):
        query = "INSERT INTO cards (title, description, position, due_date, list_id) VALUES (?, ?, ?, ?, ?)"
        self.execute_query(query, (title, description, position, due_date, list_id))
        self.data_changed.emit()
        return self.execute_query("SELECT last_insert_rowid()").fetchone()[0]

    def get_cards(self, list_id):
        query = "SELECT * FROM cards WHERE list_id = ? ORDER BY position"
        return self.execute_query(query, (list_id,)).fetchall()

    def get_card(self, card_id):
        query = "SELECT * FROM cards WHERE id = ?"
        return self.execute_query(query, (card_id,)).fetchone()

    def update_card(self, card_id, title, description, position, due_date, list_id):
        query = "UPDATE cards SET title = ?, description = ?, position = ?, due_date = ?, list_id = ? WHERE id = ?"
        self.execute_query(query, (title, description, position, due_date, list_id, card_id))
        self.data_changed.emit()

    def delete_card(self, card_id):
        queries = [
            "DELETE FROM card_labels WHERE card_id = ?",
            "DELETE FROM checklist_items WHERE checklist_id IN (SELECT id FROM checklists WHERE card_id = ?)",
            "DELETE FROM checklists WHERE card_id = ?",
            "DELETE FROM attachments WHERE card_id = ?",
            "DELETE FROM cards WHERE id = ?"
        ]
        for query in queries:
            self.execute_query(query, (card_id,))
        self.data_changed.emit()

    # Label methods
    def create_label(self, name, color, board_id):
        query = "INSERT INTO labels (name, color, board_id) VALUES (?, ?, ?)"
        self.execute_query(query, (name, color, board_id))
        self.data_changed.emit()
        return self.execute_query("SELECT last_insert_rowid()").fetchone()[0]

    def get_labels(self, board_id):
        query = "SELECT * FROM labels WHERE board_id = ?"
        return self.execute_query(query, (board_id,)).fetchall()

    def update_label(self, label_id, name, color):
        query = "UPDATE labels SET name = ?, color = ? WHERE id = ?"
        self.execute_query(query, (name, color, label_id))
        self.data_changed.emit()

    def delete_label(self, label_id):
        queries = [
            "DELETE FROM card_labels WHERE label_id = ?",
            "DELETE FROM labels WHERE id = ?"
        ]
        for query in queries:
            self.execute_query(query, (label_id,))
        self.data_changed.emit()

    def add_label_to_card(self, card_id, label_id):
        query = "INSERT OR IGNORE INTO card_labels (card_id, label_id) VALUES (?, ?)"
        self.execute_query(query, (card_id, label_id))
        self.data_changed.emit()

    def remove_label_from_card(self, card_id, label_id):
        query = "DELETE FROM card_labels WHERE card_id = ? AND label_id = ?"
        self.execute_query(query, (card_id, label_id))
        self.data_changed.emit()

    def get_card_labels(self, card_id):
        query = """
        SELECT l.* FROM labels l
        JOIN card_labels cl ON l.id = cl.label_id
        WHERE cl.card_id = ?
        """
        return self.execute_query(query, (card_id,)).fetchall()

    # Checklist methods
    def create_checklist(self, title, card_id):
        query = "INSERT INTO checklists (title, card_id) VALUES (?, ?)"
        self.execute_query(query, (title, card_id))
        self.data_changed.emit()
        return self.execute_query("SELECT last_insert_rowid()").fetchone()[0]

    def get_checklists(self, card_id):
        query = "SELECT * FROM checklists WHERE card_id = ?"
        return self.execute_query(query, (card_id,)).fetchall()

    def update_checklist(self, checklist_id, title):
        query = "UPDATE checklists SET title = ? WHERE id = ?"
        self.execute_query(query, (title, checklist_id))
        self.data_changed.emit()

    def delete_checklist(self, checklist_id):
        queries = [
            "DELETE FROM checklist_items WHERE checklist_id = ?",
            "DELETE FROM checklists WHERE id = ?"
        ]
        for query in queries:
            self.execute_query(query, (checklist_id,))
        self.data_changed.emit()

    # Checklist item methods
    def create_checklist_item(self, content, position, checklist_id):
        query = "INSERT INTO checklist_items (content, is_checked, position, checklist_id) VALUES (?, ?, ?, ?)"
        self.execute_query(query, (content, False, position, checklist_id))
        self.data_changed.emit()
        return self.execute_query("SELECT last_insert_rowid()").fetchone()[0]

    def get_checklist_items(self, checklist_id):
        query = "SELECT * FROM checklist_items WHERE checklist_id = ? ORDER BY position"
        return self.execute_query(query, (checklist_id,)).fetchall()

    def update_checklist_item(self, item_id, content, is_checked, position):
        query = "UPDATE checklist_items SET content = ?, is_checked = ?, position = ? WHERE id = ?"
        self.execute_query(query, (content, is_checked, position, item_id))
        self.data_changed.emit()

    def delete_checklist_item(self, item_id):
        query = "DELETE FROM checklist_items WHERE id = ?"
        self.execute_query(query, (item_id,))
        self.data_changed.emit()

    # Attachment methods
    def create_attachment(self, filename, file_path, card_id):
        query = "INSERT INTO attachments (filename, file_path, uploaded_at, card_id) VALUES (?, ?, ?, ?)"
        uploaded_at = datetime.now().isoformat()
        self.execute_query(query, (filename, file_path, uploaded_at, card_id))
        self.data_changed.emit()
        return self.execute_query("SELECT last_insert_rowid()").fetchone()[0]

    def get_attachments(self, card_id):
        query = "SELECT * FROM attachments WHERE card_id = ? ORDER BY uploaded_at DESC"
        return self.execute_query(query, (card_id,)).fetchall()

    def delete_attachment(self, attachment_id):
        query = "DELETE FROM attachments WHERE id = ?"
        self.execute_query(query, (attachment_id,))
        self.data_changed.emit()

    # Task methods for calendar and timeline views
    def get_user_tasks(self, user_id):
        query = """
        SELECT c.id, c.title, c.description, c.due_date, b.title as board_title, l.title as list_title
        FROM cards c
        JOIN lists l ON c.list_id = l.id
        JOIN boards b ON l.board_id = b.id
        WHERE b.user_id = ? AND c.due_date IS NOT NULL
        ORDER BY c.due_date
        """
        return self.execute_query(query, (user_id,)).fetchall()
