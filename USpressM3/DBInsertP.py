from django.http import HttpResponse
from django.shortcuts import render
import operator
import requests
from bs4 import BeautifulSoup
import sqlite3



conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()

with open ('positive-words.txt') as fp:
    for line in fp:

        line2 = line.rstrip('\n')
        SQL = "INSERT OR IGNORE INTO positivewords (words) VALUES" + "(" + "'" + line2 + "'" + ")"
        print(SQL)

        #SQL = "INSERT OR IGNORE INTO positivewords (words) VALUES('worth')"

        cur.execute(SQL)

cur.execute("select * from positivewords")
rows = cur.fetchall()
print("If you see the following, that means the DB is working!")
print(rows)

conn.commit()
conn.close()