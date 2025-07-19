
import sqlite3
import os
import bcrypt

class DatabaseManager():
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'budget_manager.db')
        self.initialize()

    def initialize(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                username UNIQUE PRIMARY KEY NOT NULL,
                name NOT NULL,
                password_hash NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_budget INTEGER
        )
    ''')
        c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                needed TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                username TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    ''')
        conn.commit()
        conn.close()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA foreign_keys = ON')
        return conn
    
    def add_column(self, table, column_name, column_type):
        conn = sqlite3.connect(self.db_path)
        conn.execute(f'ALTER TABLE {table} ADD COLUMN {column_name} {column_type.upper()}')
        conn.commit()
        conn.close()

class User():
    def __init__(self, username, name):
        self.username = username
        self.name = name
        self.db = DatabaseManager()
    @classmethod
    def sign_up(cls, username, name, password):
        """Create new user - Password is hashed immediately"""
        db = DatabaseManager()
        conn = db.get_connection()
        c = conn.cursor()
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        c.execute('INSERT INTO users (username, name, password_hash) VALUES (?,?,?)', (username, name, hashed_pw))
        conn.commit()
        conn.close()
        return cls(username=username, name=name)
    @classmethod
    def login(cls, username, password):
        """Logs in existing user"""
        db = DatabaseManager()
        conn = db.get_connection()
        c = conn.cursor()
        c.execute('SELECT password_hash, name FROM users WHERE username=?', (username,))
        row = c.fetchone()
        conn.close()
        check_password = bcrypt.checkpw(password.encode(), row[0].encode())
        if check_password:
            return cls(username=username, name=row[1])     
        return False
    
class Transaction():
    def __init__(self, username):
        self.username = username
        self.db = DatabaseManager()
    
    def add_tx(self, name, type, needed, amount):
        """Adding a transaction to a user"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO transactions (name, type, needed, username, amount) VALUES (?,?,?,?,?)', (name, type, needed, self.username, amount))
        conn.commit()
        conn.close()

    def get_tx(self):
        """Getting the user transactions"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT id, name, type, needed, created_at, amount FROM transactions WHERE username=?', (self.username,))
        transactions = c.fetchall()
        conn.close()
        return transactions

    def delete_tx(self, tx_id):
        """Deleting a transaction from a user by ID"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('DELETE FROM transactions WHERE id=? AND username=?', (tx_id, self.username))
        conn.commit()
        conn.close()

    

user1 = User.login('test', '1')
#new_tx = Transaction(user1.username, 'Dinner', 'Spending', 'Yes', 200)
#new_tx.save_to_db()
#dl_tx = Transaction(user1.username, 'Dinner', 'Spending', 'Yes', 200)
tx1 = Transaction(user1.username)


