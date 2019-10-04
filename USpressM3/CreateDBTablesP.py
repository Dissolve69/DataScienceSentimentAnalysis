import sqlite3

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()

cur.execute("create table positivewords (num INTEGER PRIMARY KEY AUTOINCREMENT, words TEXT UNIQUE, score DECIMAL)")
conn.commit()

cur.execute("select * from positivewords")
rows = cur.fetchall()
print (rows)

conn.close()