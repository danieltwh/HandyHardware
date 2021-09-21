import sqlite3
import json

with open('products.json') as f:
  data = json.load(f)

conn = sqlite3.connect('products.db')

cursor = conn.cursor()

cursor.execute('''
  CREATE TABLE products (
    Category TEXT,
    Cost REAL,
    Model TEXT,
    Price REAL,
    ProductID TEXT PRIMARY KEY,
    Warranty INTEGER);
    ''')

for row in data:
  cursor.execute('''
  INSERT INTO products VALUES (?,?,?,?,?,?)
  ''',
  [row['Category'],
  row['Cost ($)'],
  row['Model'],
  row['Price ($)'],
  row['ProductID'],
  row['Warranty (months)']]
  )

# cursor.execute('''
# CREATE TABLE items (
#  ItemID INTEGER PRIMARY KEY,
#  Category TEXT,
#  Color TEXT,
#  Factory INTEGER,
#  PowerSupply INTEGER,
#  PurchaseStatus TEXT,
#  ProductionYear INTEGER,
#  Model TEXT,
#  ServiceStatus TEXT);
# ''')

# for row in data:
#     cursor.execute('''
#     INSERT INTO items VALUES (?,?,?,?,?,?,?,?,?)
#     ''', 
#     [row['ItemID'], 
#     row['Category'],
#     row['Color'],
#     row['Factory'],
#     row['PowerSupply'],
#     row['PurchaseStatus'],
#     row['ProductionYear'],
#     row['Model'],
#     row['ServiceStatus']]
    
#     )

conn.commit()

conn.close()