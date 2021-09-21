import sqlite3

connection = sqlite3.connect('items.db')
cursor = connection.cursor()
cursor.execute('SELECT * FROM products WHERE ItemID < 1005')
print(cursor.fetchall())