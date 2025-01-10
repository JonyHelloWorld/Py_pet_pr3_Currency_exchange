import sqlite3

connection = sqlite3.connect("/DB/currency.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
    )
""")

cursor.execute("INSERT INTO name (name, age) VALUES (?, ?)", ("Jony", 48))

connection.commit()

print(cursor.execute("SELECT * FROM users"))

connection.close()