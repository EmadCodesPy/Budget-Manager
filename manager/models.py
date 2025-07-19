
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
    
