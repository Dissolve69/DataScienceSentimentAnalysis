from django.http import HttpResponse
from django.shortcuts import render

import operator
import requests
from bs4 import BeautifulSoup
import sqlite3
import re

def sentia(request):

    links = request.GET.get('links')


# 페이지 고정

# 개선 IDEA
# USAtoday 스크래핑 사이트에서 클릭으로 링크를 가져와 실행하게 함
# 프로그램 스스로 HTML tag 와 문자 구성을 파악해 사이트 종류에 상관없이 기사 내용 그리고 관련 정보를 가져올수 있게 함
# 지금은 파싱을 위해 각각 사이트 구조를 알아야 하는 번거로움이 있음

    #deeppage = 'https://usatoday.com/story/news/world/2019/08/22/south-korea-end-intelligence-sharing-deal-japan/2081846001/'
    deeppage ='https://usatoday.com/story/news/world/2019/06/30/north-korea-kim-jong-un-evade-un-sanctions-get-luxury-limo-despite-trump-maximum-pressure/1523974001/'
    #deeppage ='https://usatoday.com/story/news/nation/2019/07/04/korean-war-soldier-coming-home-after-70-years/1617460001/'

    page = requests.get(deeppage)
    soup = BeautifulSoup(page.content, 'html.parser')
    num = 1;
    content = ""
    attrsforcon = 'speakable-p-1 p-text'
    contentf = soup.find(attrs={"class": attrsforcon})

# ---------------- 문장 스크래핑 ---------------- #
    while (contentf != None):
        content += contentf.text
        num += 1
        attrsforcon = 'speakable-p-'
        attrsforcon += str(num)
        attrsforcon += ' p-text'
        contentf = soup.find(attrs={"class": attrsforcon})

    for contentf in soup.find_all(attrs={"class": "p-text"}):
        content += contentf.text
        num += 1
# ---------------- 문장 스크래핑 ---------------- #


# ---------------- Word Count ---------------- #
    wordlist = content.split()
    worddictionary = {}

    for word in wordlist:
        if word in worddictionary:
            result = re.sub('[^0-9a-zA-Zㄱ-힗]', '', word)
        # Increase
            worddictionary[result] += 1
        else:
            result = re.sub('[^0-9a-zA-Zㄱ-힗]', '', word)
        # add to the dictionary
            worddictionary[result] = 1

    sortedwords = sorted(worddictionary.items(), key=operator.itemgetter(1), reverse=True)
    print(sortedwords)

    return render(request, 'WebUSAtodaySentimentAnalysis.html', {'fulltext2': links, 'sortedwords':sortedwords})

#------------------ Basic Sentiment Analysis ------------------#
    """
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()

    PositivieNum = 0
    for word in wordlist:
        result = re.sub('[^0-9a-zA-Zㄱ-힗]', '', word)
        #print(result)
        SQL = "Select * from positivewords where  words = " + "'" + result + "'"
        cur.execute (SQL)
        rows = cur.fetchall()
        if rows:
            PositivieNum += 1
            print(rows)
    #print("This article includes:", PositivieNum , "Positive words")
    print("###########################################")

    NegativeNum = 0
    for word in wordlist:
        result = re.sub('[^0-9a-zA-Zㄱ-힗]', '', word)
        SQL = "Select * from negativewords where words = " + "'" + result + "'"
        cur.execute (SQL)
        rows = cur.fetchall()
        if rows:
            NegativeNum += 1
            print(rows)
    #print("This article includes:", NegativeNum , "Negative words")

    conn.close()

    print("This article includes total:", len(wordlist), "words")
    print("This article includes:", PositivieNum , "Positive words and",NegativeNum, "Negative words") 
    """