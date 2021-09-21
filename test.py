import sqlite3

connection = sqlite3.connect('items.db')
cursor = connection.cursor()
print(cursor.fetchall())