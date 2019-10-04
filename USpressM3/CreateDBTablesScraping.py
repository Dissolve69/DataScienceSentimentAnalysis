import sqlite3

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()


cur.execute("create table scraping (num INTEGER PRIMARY KEY AUTOINCREMENT, publisher TEXT, date TEXT, title TEXT, author TEXT, links TEXT UNIQUE ON CONFLICT IGNORE, contents TEXT)")
conn.commit()

cur.execute("select * from scraping")
rows = cur.fetchall()
print (rows)

conn.close()