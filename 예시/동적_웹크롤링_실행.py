import time
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


#step2.검색할 키워드 입력
query = input('검색할 키워드를 입력하세요: ')


# 크롬 옵션 설정
options = ChromeOptions()
options.add_experimental_option("detach", True)

# 웹드라이버 설정 및 실행
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

#step3.크롬드라이버로 원하는 url로 접속
url = 'https://www.naver.com/'
driver.get(url)
time.sleep(5)  # 페이지 로딩 대기

# 검색어 창을 찾아 search 변수에 저장 (By.XPATH 방식)
search_box = driver.find_element(By.XPATH, '//*[@id="query"]')
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)
time.sleep(5)  # 검색 결과 확인을 위해 대기
driver.find_element(By.XPATH, '//*[@id="lnb"]/div[1]/div/div[1]/div/div[2]/div[2]/a/span/i').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="lnb"]/div[1]/div/div[1]/div/div[1]/div[8]/a').click()
time.sleep(2)


#step6.뉴스 제목 텍스트 추출

news_titles = driver.find_elements(By.CLASS_NAME, "news_tit")

for i in news_titles:
    title = i.text
    print(title)

#step7.뉴스 하이퍼링크 추출

for i in news_titles:
    href = i.get_attribute('href')
    print(href)

#step8.뉴스 썸네일 이미지 추출

# 스크롤 내리기 (모든 썸네일 이미지 로딩을 위함)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

time.sleep(2)

#뉴스 썸네일 이미지 다운로드
news_content_div = driver.find_elements(By.CLASS_NAME, 'news_contents')

news_thumbnail = []

for i in news_content_div:

    try:

        thumbnail = i.find_element(By.CLASS_NAME, "thumb")
        news_thumbnail.append(thumbnail)

    except:
        pass

link_thumbnail = [img.get_attribute('src')for img in news_thumbnail]

# 이미지 저장할 폴더 생성
import os

# path_folder의 경로는 각자 저장할 폴더의 경로를 적어줄 것
path_folder = r'C:\interncrawl\eximg/'

if not os.path.isdir(path_folder):
    os.mkdir(path_folder)

# 이미지 다운로드
from urllib.request import urlretrieve

i = 0

for link in link_thumbnail:
    i += 1
    urlretrieve(link, path_folder + f'{i}.jpg')
    time.sleep(0.3)





# 브라우저가 자동으로 닫히지 않도록 대기
input("Press Enter to continue...")