import sqlite3

connection = sqlite3.connect('products.db')
cursor = connection.cursor()
cursor.execute('SELECT * FROM products')
print(cursor.fetchall())