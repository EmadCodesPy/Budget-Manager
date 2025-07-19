import sqlite3
import bcrypt
import os


def get_connection():
    BASE_DIR = os.path.dirname(__file__)
    db_path = os.path.join(BASE_DIR, 'budget_manage.db')
    conn = sqlite3.connect(db_path)
    return conn
def initialize():
    conn = sqlite3.connect('budget_manager.db')
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
    
def create_user(username, name, password):
    conn = get_connection()
    c = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    c.execute('INSERT INTO users (username, name, password) VALUES (?,?,?)', (username, name, hashed_pw))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize()