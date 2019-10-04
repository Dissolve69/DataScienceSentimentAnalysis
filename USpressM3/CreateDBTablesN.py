import sqlite3

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()

cur.execute("create table negativewords (num INTEGER PRIMARY KEY AUTOINCREMENT, words TEXT UNIQUE, score DECIMAL)")
conn.commit()

cur.execute("select * from negativewords")
rows = cur.fetchall()
print (rows)

conn.close()