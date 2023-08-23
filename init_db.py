import sqlite3

connection = sqlite3.connect('store.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users ( firstname,lastname, password,email) VALUES (?, ?, ?, ?)",
            ('ivan', 'ivanov', 'admin',  'admin@admin.com')
            )

connection.commit()
connection.close()
