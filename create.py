import sqlite3
query = """CREATE TABLE items (item VARCHAR(20), quantity REAL, price REAL);"""
connection = sqlite3.connect('item.db')
connection.execute(query)
connection.commit()
items = [('rice', 5.0, 5.20), ('milk', 2.0, 5.65), ('pork', 3.0, 10.80), ('coke', 30.0, 0.90),
('fish', 2.50, 2.50)]
statement = "INSERT INTO items VALUES(?, ?, ?)"
connection.executemany(statement, items)
connection.commit()

