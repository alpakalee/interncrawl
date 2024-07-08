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
time.sleep(10)  # 페이지 로딩 대기

# 검색어 창을 찾아 search 변수에 저장 (By.XPATH 방식)
search_box = driver.find_element(By.XPATH, '//*[@id="query"]')
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)
time.sleep(10)  # 검색 결과 확인을 위해 대기

driver.find_element(By.XPATH, '//*[@id="lnb"]/div[1]/div/div[1]/div/div[1]/div[8]/a').click()
time.sleep(2)
# 브라우저가 자동으로 닫히지 않도록 대기
input("Press Enter to continue...")