The web app is a budget manager made using OOP, sqlite3 and streamlit:

-It must be able to CRUD (create, read, update, delete)
-input amount of money, and then amount of months you want it to last
-be able to add costs that will be subtracted from the monthly budget
-show how much is left each month
-be able to add income to each month
-~~see what transactions you've made~~
-~~remove transactions~~
-know if transaction was good or bad (green or red)
-count number of good and bad spending
-show any type of chart that shows spending
-must be able to clear all info
-----------------------------------------------------------
For the DB made with sqlite3:
-~~must be a users DB with (username(UNIQUE), name, password_hash, created_at)~~
-~~must be a transaction DB with (id(PRIMARY KEY AUTOINCREMENT), name, type(spending or earning), needed, created_at, username,~~
                                ~~(FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE))~~
