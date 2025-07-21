
import sqlite3
import os
import bcrypt
import datetime

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
                amount INTEGER NOT NULL,
                month TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                username TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    ''')
        c.execute('''CREATE TABLE IF NOT EXISTS monthly_budget (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  month TEXT,
                  amount REAL,
                  FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )''')
        conn.commit()
        conn.close()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA foreign_keys = ON')
        return conn
    
    def add_column(self, table: str, column_name: str, column_type: str) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(f'ALTER TABLE {table} ADD COLUMN {column_name} {column_type.upper()}')
        conn.commit()
        conn.close()

class User():
    def __init__(self, username: str, name: str):
        self.username = username
        self.name = name
        self.db = DatabaseManager()

    @classmethod
    def sign_up(cls, username: str, name: str, password: str) -> classmethod:
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
    def login(cls, username: str, password: str) -> classmethod:
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
    

    def delete_account(self) -> None:
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('DELETE FROM users WHERE username=?', (self.username,))
        conn.commit()
        conn.close()
    
class Transaction():
    def __init__(self, username: str):
        self.username = username
        self.db = DatabaseManager()
    
    
    def add_tx(self, name: str, type: str, amount: int) -> None:
        """Adding a transaction to a user"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO transactions (name, type, username, amount) VALUES (?,?,?,?)', (name, type, self.username, amount))
        conn.commit()
        conn.close()

    def get_tx(self, month: str) -> list:
        """Getting the user transactions"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT id, name, type, needed, created_at, amount FROM transactions WHERE username=? AND month=?', (self.username, month))
        transactions = c.fetchall()
        conn.close()
        return transactions

    def delete_tx(self, tx_id: int) -> None:
        """Deleting a transaction from a user by ID"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('DELETE FROM transactions WHERE id=? AND username=?', (tx_id, self.username))
        conn.commit()
        conn.close()
    
    def allocate_budget(self, budget: int, months: int) -> None:
        monthly_budget = round(budget / months, 1)
        conn = self.db.get_connection()
        c = conn.cursor()
        for i in range(months):
            month_name = datetime.date.today().replace(day=1).replace(month=(datetime.date.today().month + i-1)%12 + 1).strftime('%B')
            c.execute('INSERT OR REPLACE INTO monthly_budget (username, month, amount) VALUES (?,?,?)', (self.username, month_name, monthly_budget))
        conn.commit()
        conn.close()
    
    def delete_budget(self):
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('DELETE FROM monthly_budget WHERE username=?', (self.username,))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    #user = User.sign_up('test','test','1')
    #user = User.login('test', '1')
    #tx = Transaction(user.username)
    pass