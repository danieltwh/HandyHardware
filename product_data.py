import sqlite3
import sqlite3
import json

with open('products.json') as f:
  data = json.load(f)

conn = sqlite3.connect('products.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE items (
 Category TEXT,
 Cost INTEGER,
 Model TEXT,
 Price INTEGER,
 ProductID INTEGER,
 Warranty INTEGER);
''')

for row in data:
    cursor.execute('''
    INSERT INTO items VALUES (?,?,?,?,?,?)
    ''', 
    [row['Category'],
    row['Cost'],
    row['Model'],
    row['Price'],
    row['ProductID'],
    row['Warranty']]
    )

conn.commit()

conn.close()