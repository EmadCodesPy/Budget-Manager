
import sqlite3
import os
import bcrypt
import datetime
from exceptions import UsernameInUseError
from dateutil.relativedelta import relativedelta


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
                month TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                username TEXT NOT NULL,
                FOREIGN KEY (username, month) REFERENCES monthly_budget(username, month) ON DELETE CASCADE
        )
    ''')
        c.execute('''CREATE TABLE IF NOT EXISTS monthly_budget (
                  username TEXT NOT NULL,
                  month TEXT NOT NULL,
                  amount REAL NOT NULL,
                  PRIMARY KEY (username, month),
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
        conn.commit()
        conn.close()
        return cls(username=username, name=name)
        
    @classmethod
    def login(cls, username: str, password: str) -> classmethod:
        """Logs in existing user by comparing username and password to the database"""
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
        """Deletes all details of an account from the database"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('DELETE FROM users WHERE username=?', (self.username,))
        conn.commit()
        conn.close()
    
class Transaction():
    def __init__(self, username: str)  -> None:
        self.username = username
        self.db = DatabaseManager()
    
    def add_tx(self, name: str, type: str, amount: int, month: str) -> None:
        """Adding a transaction to a user: Takes the name of the transaction, the type, the amount, and the month it was made in"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO transactions (name, type, username, amount, month) VALUES (?,?,?,?,?)', (name, type, self.username, amount, month))
        if type == 'Earning':
            monthly_budget = self.get_monthly_budget(month) + amount
            #total_budget = self.get_total_budget() + amount
            c.execute('UPDATE monthly_budget SET amount=? WHERE username=? AND month=?', (monthly_budget, self.username, month))
            #c.execute('UPDATE users SET total_budget=? WHERE username=?', (total_budget, self.username))
        elif type == 'Spending':
            monthly_budget = self.get_monthly_budget(month) - amount
            #total_budget = self.get_total_budget() - amount
            c.execute('UPDATE monthly_budget SET amount=? WHERE username=? AND month=?', (monthly_budget, self.username, month))
            #c.execute('UPDATE users SET total_budget=? WHERE username=?', (total_budget, self.username))
        conn.commit()
        conn.close()

    def get_tx(self, month: str) -> dict:
        """Getting the user transactions in a certain month. Gets the [id, name, type, amount, month, created_at]"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT id, name, type, amount, month, created_at FROM transactions WHERE username=? AND month=?', (self.username, month))
        columns = [col[0] for col in c.description]
        all_transactions = [dict(zip(columns, row)) for row in c.fetchall()]
        conn.close()
        return all_transactions

    def delete_tx(self, tx_id: int = 0, month: str = None, all: bool = False) -> None:
        """Deleting a transaction from a user by ID"""
        conn = self.db.get_connection()
        c = conn.cursor()
        #Delete all transactions
        if all == True:
            c.execute('DELETE FROM transactions WHERE username=?', (self.username,))
            conn.commit()
            conn.close()
            return
        
        #Select total budget for a user
        c.execute('SELECT total_budget FROM users WHERE username=?', (self.username,))
        #Comma exists because it returns a tuple. If there is no comma it will not unpack the tuple and current_budget[0] will need to be used
        (current_total_budget,) = c.fetchone()

        #Select transaction info for a transaction
        c.execute('SELECT type, amount FROM transactions WHERE id=? AND username=?', (tx_id, self.username))
        tx_row = c.fetchone()

        #Select amount in monthly_budget
        c.execute('SELECT amount FROM monthly_budget WHERE username=? AND month=?', (self.username, month))
        (current_monthly_budget,) = c.fetchone()

        #Update the total_budget from the users table and amount from the monthly_budget table
        if tx_row:
            type_, amount = tx_row
            if type_ == 'Spending':  
                new_total_budget = current_total_budget + amount
                new_monthly_budget = current_monthly_budget + amount
            elif type_ == 'Earning':
                new_total_budget = current_total_budget - amount
                new_monthly_budget = current_monthly_budget - amount
            #Update the total budget
            c.execute('UPDATE users SET total_budget=? WHERE username=?', (new_total_budget, self.username))
            c.execute('UPDATE monthly_budget SET amount=? WHERE username=? AND month=?', (new_monthly_budget, self.username, month))
        
        c.execute('DELETE FROM transactions WHERE id=? AND username=?', (tx_id, self.username))
        
        conn.commit()
        conn.close()
    
    def allocate_budget(self, budget: int, months: int) -> None:
        """Allocates a total budget to a users account. It is possible"""
        monthly_budget = round(budget / months, 1)
        today = datetime.date.today()

        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('UPDATE users SET total_budget=? WHERE username=?', (budget, self.username))
        for i in range(months):
            # Adds i months to current date
            month_date = today + relativedelta(months=i)
            # Format 2025-January
            month_key = month_date.strftime('%Y-%B')
            c.execute('INSERT OR REPLACE INTO monthly_budget (username, month, amount) VALUES (?,?,?)', (self.username, month_key, monthly_budget))
        
        conn.commit()
        conn.close()
    
    def delete_budget(self) -> None:
        """Removes all budget information from monthly_budget table"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('DELETE FROM monthly_budget WHERE username=?', (self.username,))
        c.execute('UPDATE users SET total_budget=? WHERE username=?', (None, self.username))
        conn.commit()
        conn.close()

    def get_monthly_budget(self, month: str) -> int:
        """Returns the monthly budget for the month passes into month parameter"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT amount FROM monthly_budget WHERE username=? AND month=?', (self.username, month))
        result = c.fetchone()
        conn.close()
        return result[0]
    
    def get_months(self) -> list[str]:
        """Gets all the months that is in the monthly_budget table by username"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT month FROM monthly_budget WHERE username=?', (self.username,))
        result = c.fetchall()
        conn.close()
        if result is None:
            return False
        return [month[0] for month in result]

    def get_total_budget(self) -> int:
        """Returns the total budget of a user"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT total_budget FROM users WHERE username=?', (self.username,))
        result = c.fetchone()
        conn.close()
        if result[0] is None:
            return 0
        return result[0]

    def get_monthly_cash_flow(self, type: str = ['Spending', 'Earning'], month: str = None) -> int:
        """Gets the total monthly spending or earning of a user"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT amount FROM transactions WHERE username=? AND type=? AND month=?', (self.username, type, month))
        result = c.fetchall()
        conn.close()
        if result is None:
            return 0
        return sum([x[0] for x in result])

    def get_total_cash_flow(self, type: str = ['Spending', 'Earning']) -> int:
        """Gets the total spending or earning of a user"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT amount FROM transactions WHERE username=? AND type=?', (self.username, type))
        result = c.fetchall()
        conn.close()
        if result is None:
            return 0
        return sum([x[0] for x in result])

    def get_fixed_monthly_budget(self) -> int:
        """Returns the monthly budget of each month, without including transactions made. The original fixed budget"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT total_budget FROM users WHERE username=?', (self.username,))
        row = c.fetchone()
        total_budget = row[0]if row else 0
        c.execute('SELECT month FROM monthly_budget WHERE username=?', (self.username,))
        row = c.fetchall()
        number_of_months = len(row) if row else 0
        conn.close()
        fixed_monthly_budget = total_budget/number_of_months
        return fixed_monthly_budget

    def tx_piechart(self, month: str) -> list:
        """Return the names and amounts of transactions as two lists: tx_names, tx_amount"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT name, amount FROM transactions WHERE username=? AND month=?', (self.username, month))
        result = c.fetchall()
        conn.close()
        tx_names = [x[0] for x in result]
        tx_amount = [x[1] for x in result]
        return tx_names, tx_amount

    def recent_tx(self, length: int) -> list[tuple]:
        """Returns the most recent transactions (name, amount, type) up to the length parameter. (Assumes everything is entered in order)"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT name, amount, type FROM transactions WHERE username=?', (self.username,))
        result = c.fetchall()
        conn.close()
        most_recent_tx = result[::-1][:length]
        return most_recent_tx

    def budget_progress(self, include_numbers: bool = False) -> int:
        """Returns the ratio of amount spent and total budget (ratio). If include_numbers is True, it will also return the amount spend and the total_budget (ratio, amount_spent, total_budget)"""
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('SELECT total_budget FROM users WHERE username=?', (self.username,))
        total_budget = c.fetchone()
        c.execute('SELECT amount FROM transactions WHERE username=? AND type=?', (self.username, 'Spending'))
        amount_spent_total = c.fetchall()
        amount_spent = sum([x[0] for x in amount_spent_total])
        conn.close()
        ratio = (amount_spent / total_budget[0])
        if include_numbers:
            return ratio, amount_spent, total_budget[0]
        return ratio


if __name__ == '__main__':
    user = User.login('test', '1')
    tx = Transaction(user.username)
    pass