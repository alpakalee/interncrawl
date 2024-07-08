import requests
from bs4 import BeautifulSoup

# 웹 페이지 요청
url = "https://www.sojoong.kr/www/"
response = requests.get(url)
html_content = response.content

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_content, 'html.parser')

# HTML 파싱 및 데이터 추출
# 예시 1: 모든 <h1> 태그의 텍스트 추출
for h1_tag in soup.find_all('h1'):
    print(h1_tag.text)

# 예시 2: 특정 클래스명을 가진 <div> 태그의 텍스트 추출
for div_tag in soup.find_all('div', class_='example-class'):
    print(div_tag.text)

# 예시 3: 특정 아이디를 가진 요소 추출
#element = soup.find(id='example-id')
#print(element.text)
print("-----")
# 예시 4: 특정 속성을 가진 태그 추출
for link in soup.find_all('a', href=True):
    print(link['href'])
