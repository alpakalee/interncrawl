# step1.프로젝트에 필요한 패키지 불러오기

from bs4 import BeautifulSoup as bs

import requests


# step2. 검색할 키워드 입력

query = input('검색할 키워드를 입력하세요: ')


# step3. 입력받은 query가 포함된 url 주소(네이버 뉴스 검색 결과 페이지) 저장

url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query='+'%s'%query


# step4. requests 패키지를 이용해 'url'의 html 문서 가져오기

response = requests.get(url)

html_text = response.text


# step5. beautifulsoup 패키지로 파싱 후, 'soup' 변수에 저장

soup = bs(response.text, 'html.parser')

#step6.뉴스 제목 텍스트 추출
news_titles = soup.select("a.news_tit")

for i in news_titles:
    title = i.get_text()
    print(title)
    href = i.attrs['href']
    print(href)

#step7.뉴스 하이퍼링크 추출

#for i in news_titles:
#    href = i.attrs['href']
#    print(href)

#step8.뉴스 썸네일 이미지 추출

news_content_div = soup.select(".news_contents")

news_thumbnail = [thumbnail.select_one(".thumb") for thumbnail in news_content_div]

link_thumbnail = []

for img in news_thumbnail:
    if img is  not  None  and  'data-lazysrc'  in img.attrs:
        link_thumbnail.append(img.attrs['data-lazysrc'])

# 이미지 저장할 폴더 생성
import os

# path_folder의 경로는 각자 저장할 폴더의 경로를 적어줄 것(ex.img_download)
path_folder = 'C:\interncrawl\eximg/'

if not os.path.isdir(path_folder):
    os.mkdir(path_folder)

# 이미지 다운로드
from urllib.request import urlretrieve

i = 0

for link in link_thumbnail:          
    i += 1
    urlretrieve(link, path_folder + f'{i}.jpg')


