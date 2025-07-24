
import sqlite3
import os
import bcrypt
import datetime
from exceptions import UsernameInUseError



class DatabaseManager():
    def __init__(self) -> None:
        self.db_path = os.path.join(os.path.dirname(__file__), 'budget_manager.db')
        self.initialize()

    def initialize(self) -> None:
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
    
    def get_connection(self) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA foreign_keys = ON')
        return conn
    
    def add_column(self, table: str, column_name: str, column_type: str) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(f'ALTER TABLE {table} ADD COLUMN {column_name} {column_type.upper()}')
        conn.commit()
        conn.close()

class User():
    def __init__(self, username: str, name: str) -> None:
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
        try:
            c.execute('INSERT INTO users (username, name, password_hash) VALUES (?,?,?)', (username, name, hashed_pw))
        except sqlite3.IntegrityError:
            conn.close()
            raise UsernameInUseError('Username is already in use')
        for month in [datetime.date(2025, month, 1).strftime('%B') for month in range(1,13)]:
            c.execute('INSERT INTO monthly_budget (username, month, amount)  VALUES (?,?,?)', (username, month, 0))
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
        if row is None:
            return False
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
    
    def account_start_date(self) -> str:
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT created_at FROM users WHERE username=?', (self.username,))
        result = c.fetchone()
        return result[0]

class Transaction():
    def __init__(self, username: str)  -> None:
        self.username = username
        self.db = DatabaseManager()
    
    def add_tx(self, name: str, type: str, amount: int, month: str) -> None:
        """Adding a transaction to a user"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO transactions (name, type, username, amount, month) VALUES (?,?,?,?,?)', (name, type, self.username, amount, month))
        if type == 'Earning':
            monthly_budget = self.get_monthly_budget(month) + amount
            total_budget = self.get_total_budget() + amount
            c.execute('UPDATE monthly_budget SET amount=? WHERE username=? AND month=?', (monthly_budget, self.username, month))
            c.execute('UPDATE users SET total_budget=? WHERE username=?', (total_budget, self.username))
        elif type == 'Spending':
            monthly_budget = self.get_monthly_budget(month) - amount
            total_budget = self.get_total_budget() - amount
            c.execute('UPDATE monthly_budget SET amount=? WHERE username=? AND month=?', (monthly_budget, self.username, month))
            c.execute('UPDATE users SET total_budget=? WHERE username=?', (total_budget, self.username))
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

    def delete_tx(self, tx_id: int = 0, all: bool = False) -> None:
        """Deleting a transaction from a user by ID"""
        conn = self.db.get_connection()
        c = conn.cursor()
        if all == True:
            c.execute('DELETE FROM transactions WHERE username=?', ( self.username,))
        elif all == False:
            c.execute('SELECT (type, amount) FROM transactions WHERE id=? AND username=?', (tx_id, self.username))
            result = c.fetchone()
            if result[0] == 'Spending':
                total_budget = self.get_total_budget() + result[1]
                c.execute('UPDATE users SET total_budget=? WHERE username=?', (total_budget, self.username))
            elif result[0] == 'Earning':
                total_budget = self.get_total_budget() - result[1]
                c.execute('UPDATE users SET total_budget=? WHERE username=?', (total_budget, self.username))
        c.execute('DELETE FROM transactions WHERE id=? AND username=?', (tx_id, self.username))
        conn.commit()
        conn.close()
    
    def allocate_budget(self, budget: int, months: int, refactor: bool = False) -> None:
        monthly_budget = round(budget / months, 1)
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('UPDATE users SET total_budget=? WHERE username=?', (budget, self.username))
        for i in range(months):
            month_name = datetime.date.today().replace(day=1).replace(month=(datetime.date.today().month + i-1)%12 + 1).strftime('%B')
            c.execute('INSERT OR REPLACE INTO monthly_budget (username, month, amount) VALUES (?,?,?)', (self.username, month_name, monthly_budget))
        conn.commit()
        conn.close()
    
    def delete_budget(self) -> None:
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('DELETE FROM monthly_budget WHERE username=?', (self.username,))
        conn.commit()
        conn.close()

    def get_monthly_budget(self, month: str) -> int:
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT amount FROM monthly_budget WHERE username=? AND month=?', (self.username, month))
        result = c.fetchone()
        return result[0]
    
    def get_months(self) -> list:
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT month FROM monthly_budget WHERE username=?', (self.username,))
        result = c.fetchall()
        if result is None:
            return False
        return [month[0] for month in result]

    def get_total_budget(self) -> int:
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT total_budget FROM users WHERE username=?', (self.username,))
        result = c.fetchone()
        if result[0] is None:
            return 0
        return result[0]

    def get_total_spending(self) -> int:
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT amount FROM transactions WHERE username=? AND type=?', (self.username, 'Spending'))
        result = c.fetchall()
        if result is None:
            return 0
        return sum([x[0] for x in result])

    def get_total_earning(self) -> int:
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT amount FROM transactions WHERE username=? AND type=?', (self.username, 'Earning'))
        result = c.fetchall()
        if result is None:
            return 0
        return sum([x[0] for x in result])

if __name__ == '__main__':
    #user = User.sign_up('test','test','1')
    user = User.login('test', '1')
    tx = Transaction(user.username)
    #tx.allocate_budget(500, 6)
    tx.delete_budget()
    tx.delete_tx(all=True)
    #tx.add_tx('Lunch', 'Earning', 8, 'July')
    pass