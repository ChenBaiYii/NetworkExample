import sqlite3

db = sqlite3.connect("bank.db")
# print(db.cursor())

result = db.execute("SELECT name FROM sqlite_master WHERE type='table';")

print(result.fetchall())
