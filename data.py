import sqlite3
import sqlite3
import json

with open('items.json') as f:
  data = json.load(f)

conn = sqlite3.connect('items.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE items (
 ItemID INTEGER PRIMARY KEY,
 Category TEXT,
 Color TEXT,
 Factory INTEGER,
 PowerSupply INTEGER,
 PurchaseStatus TEXT,
 ProductionYear INTEGER,
 Model TEXT,
 ServiceStatus TEXT);
''')

for row in data:
    cursor.execute('''
    INSERT INTO items VALUES (?,?,?,?,?,?,?,?,?)
    ''', 
    [row['ItemID'], 
    row['Category'],
    row['Color'],
    row['Factory'],
    row['PowerSupply'],
    row['PurchaseStatus'],
    row['ProductionYear'],
    row['Model'],
    row['ServiceStatus']]
    
    )

conn.commit()

conn.close()