# requests 패키지 가져오기
import requests   
# BeautifulSoup 패키지 불러오기
# 주로 bs로 이름을 간단히 만들어서 사용함
from bs4 import BeautifulSoup as bs            

# 가져올 url 문자열로 입력
url = 'https://www.naver.com'  

# requests의 get함수를 이용해 해당 url로 부터 html이 담긴 자료를 받아옴
response = requests.get(url)    

# 우리가 얻고자 하는 html 문서가 여기에 담기게 됨
html_text = response.text




# html을 잘 정리된 형태로 변환
html = bs(html_text, 'html.parser')

# 태그 이름으로 찾기
soup.find('p')

# 태그 속성(class)으로 찾기 - 2가지 형식
soup.find(class_='para') #이 형식을 사용할 때는 class 다음에 언더바_를 꼭 붙여주어야 한다
soup.find(attrs = {'class':'para'}) 

# 태그 속성(id)으로 찾기 - 2가지 형식
soup.find(id='zara') 
soup.find(attrs = {'id':'zara'})

# 태그 이름과 속성으로 찾기
soup.find('p', class_='para')
soup.find('div', {'id' : 'zara'})

#----------------------------------------#

# a태그의 class 속성명이 news_tit인 태그 
soup.select_one('a.news_tit')

soup.select('a.news_tit')

for i in titles: 
    title = i.get_text() 
print(title)
