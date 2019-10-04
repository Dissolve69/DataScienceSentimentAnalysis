from django.http import HttpResponse
from django.shortcuts import render
import operator
import requests
from bs4 import BeautifulSoup


def presentation(request):
    return render(request, 'presentation.html')


def homepage(request):

############### USAtoday

    # HTML 화면으로 파이썬 변수 값 개별적 넘길때 필요
    Usatodaystitles = []
    Usatodayslinks = []
    Usatodaysdates = []
    Usatodaysauthors = []
    Usatodayscontents = []
    links= []

    # 리스트 안 리스트 형식으로 묶어서 출력할때 필요
    USAtodays =[]


    for page in range(1, 2):

        changepage = "https://www.usatoday.com/search/?q=Korea&page="
        changepage += str(page)
        # print("page = ",changepage)
        page = requests.get(changepage)
        soup = BeautifulSoup(page.content, 'html.parser')
        usatoday = soup.select('div.gnt_se_hl')

        for usatodaystitle in usatoday:

            # 이 화면에서 저자, 날짜 빼오기

            dtby = usatodaystitle.parent.find(attrs={"class": "gnt_se_dtby"})
            if (dtby != None):

                UsatodaysAuthor = dtby.get('data-c-by')
                ArticleDate = dtby.get('data-c-dt')
                UsatodaysArticlelinks = usatodaystitle.parent.parent.get('href')
                UsatodaysArticlelinks2 = "https://usatoday.com" + UsatodaysArticlelinks
            # DB SQL 입력할때 Title 내에서 ' 삭제 Noapostrophe
            # Noapostrophe = title.text.replace("'", "")
                links.append(UsatodaysArticlelinks2)
                USAtodays.append([ArticleDate, usatodaystitle.text, UsatodaysAuthor, UsatodaysArticlelinks2])

            Usatodaystitles.append(usatodaystitle.text)
            #Usatodaysdates.append(ArticleDate)
            #Usatodaysauthors.append(Author)
            #Usatodayslinks.append(Articlelinks)
            
        return render(request, 'index.html', {'USAtodays': USAtodays, 'links': links,                                 'titles':Usatodaystitles}) 

