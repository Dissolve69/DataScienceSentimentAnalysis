from django.http import HttpResponse
from django.shortcuts import render

import operator
import requests
from bs4 import BeautifulSoup
import sqlite3
import re

def sentia(request):

    links = request.GET.get('links')
    positivewordslist=[]
    negativewordslist=[]


    deeppage =links
    #deeppage ='https://usatoday.com/story/news/nation/2019/07/04/korean-war-soldier-coming-home-after-70-years/1617460001/'
    page = requests.get(deeppage)
    soup = BeautifulSoup(page.content, 'html.parser')
    

# --- authors, title, dates --- #
    
    title = soup.find(attrs={"class": "asset-headline speakable-headline"}).text
    author = soup.find(attrs={"class": "asset-metabar-author asset-metabar-item"}).text
    # , 뒤에 (special to USA TODAY 이런거 삭제 원할 시 밑에 주석 풀어주시면 됩니다)
    #authortmp = author.split(",")
    #author = authortmp[0]
    date = soup.find(attrs={"class": "asset-metabar-time asset-metabar-item nobyline"}).text
    #date 도 update 말고 published 만 띄우고 싶으시면 아래 주석 풀어주시면 됩니다
    datetmp = date.split("|")
    date = datetmp[0].strip()
    
        
# --- authors, title, dates --- #
    
    
# ---------------- 문장 스크래핑 ---------------- #

    num = 1;
    content = ""
    attrsforcon = 'speakable-p-1 p-text'
    contentf = soup.find(attrs={"class": attrsforcon})

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
   # print(sortedwords)
   # print(links);


#------------------ Basic Sentiment Analysis ------------------#
   
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()

    PositiveNum = 0
    for word in wordlist:
        result = re.sub('[^0-9a-zA-Zㄱ-힗]', '', word)
        #print(result)
        SQL = "Select * from positivewords where  words = " + "'" + result + "'"
        cur.execute (SQL)
        rows = cur.fetchall()
        if rows:
            PositiveNum += 1
            positivewordslist.append(rows)
    #        print(rows)
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
            negativewordslist.append(rows)
    
    conn.close()    
    
 #

    if (PositiveNum+NegativeNum!=0):
        posPercent = ((PositiveNum/(PositiveNum+NegativeNum))*100)
        if posPercent>=70:
            print("긍정 내용의 기사입니다, 정확도 {}%".format(round(posPercent)))
            #posNeg = "관련 주제 긍정 내용 기사일 확률이 높습니다, 정확도 {}%".format(round(posPercent))
            posNeg = "관련 주제 긍정 내용 기사일 확률이 높습니다"
        elif posPercent<=30:
            print("부정 내용의 기사입니다, 정확도 {}%".format(100-round(posPercent)))
            #posNeg = "관련 주제 부정 내용 기사일 확률이 높습니다, 정확도 {}%".format(100-round(posPercent))
            posNeg = "관련 주제 부정 내용 기사일 확률이 높습니다"
        else :
            print("중립 내용의 기사입니다, 정확도 {}%".format(100-(abs(50-round(posPercent)))))
            #posNeg = "관련 주제 중립 내용 기사일 확률이 높습니다, 정확도 {}%".format(100-(abs(50-round(posPercent))))
            posNeg = "관련 주제 중립 내용 기사일 확률이 높습니다"
    else:
        posNeg = "긍정 부정 관련 단어 파악할 수 없습니다. Positive = 0, Negative = 0"
        
    return render(request, 'WebUSAtodaySentimentAnalysis.html', {'links': links, 'sortedwords': sortedwords, 'PositiveNum': PositiveNum, 'NegativeNum': NegativeNum, 'Totalwords':len(wordlist), 'PosorNeg': posNeg, 'positivewordslist':positivewordslist, 'negativewordslist':negativewordslist, 'title':title, 'date':date, 'author':author })
  
