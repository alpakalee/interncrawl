import time
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 옵션 설정
options = ChromeOptions()
options.add_experimental_option("detach", True)

# 웹드라이버 설정 및 실행
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 구글 웹사이트 열기
driver.get('https://www.google.co.kr/')
time.sleep(3)  # 페이지 로딩 대기

# 검색어 창을 찾아 search 변수에 저장 (By.XPATH 방식)
search_box = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
search_box.send_keys('파이썬')
search_box.send_keys(Keys.RETURN)
time.sleep(10)  # 검색 결과 확인을 위해 대기

# 브라우저가 자동으로 닫히지 않도록 대기
input("Press Enter to continue...")