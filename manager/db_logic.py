import sqlite3
import bcrypt

def initialize():
    conn = sqlite3.connect('budget_manager.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
              username UNIQUE PRIMARY KEY NOT NULL,
              name NOT NULL,
              password_hash NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    
if __name__ == '__main__':
    initialize()