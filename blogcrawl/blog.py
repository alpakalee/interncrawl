from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service as ChromeService #크롬으로 열기
from selenium.webdriver import ChromeOptions #크롬 옵션

# keyword = input("검색할 키워드를 입력하세요: ")
keyword = "웨딩플래너"

def driversetup(url):
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    
    # 로컬에 저장된 ChromeDriver 경로를 지정
    driver_path = "./chromedriver.exe"  # chromedriver.exe 파일이 스크립트와 동일한 디렉토리에 존재.
    driver = webdriver.Chrome(service=ChromeService(driver_path), options=options)
    driver.get(url)
    time.sleep(3)
    return driver
# 네이버 검색 페이지 접근
naver_url = 'https://www.naver.com'

driver = driversetup(naver_url)

# 검색창 찾기
search_box = driver.find_element(By.NAME, 'query')

# 키워드 입력 및 검색

search_box.send_keys(keyword)
search_box.send_keys(Keys.RETURN)

# 블로그 탭으로 이동
time.sleep(2)  # 페이지 로딩 대기
blog_tab = driver.find_element(By.CSS_SELECTOR, 'a[href*="?ssc=tab.blog.all"]')
blog_tab.click()


# 최신순 정렬 옵션 선택
time.sleep(2)  # 페이지 로딩 대기
latest_option = driver.find_element(By.XPATH, '//a[@role="option" and contains(text(), "최신순")]')
latest_option.click()


# 블로그 리스트 크롤링
time.sleep(2)  # 페이지 로딩 대기
blog_posts = driver.find_elements(By.CLASS_NAME, 'bx')
time.sleep(2) 
blog_links = []
for post in blog_posts:
    try:
        if 'user_info' in post.get_attribute('innerHTML'):
            user_info = post.find_element(By.CLASS_NAME, 'user_info')
            link = user_info.find_element(By.TAG_NAME, 'a').get_attribute('href')
            blog_links.append(link)
    except:
        print("user_info 또는 링크를 찾을 수 없습니다.")
# 결과 출력
for i, blog in enumerate(blog_links):
    print(f"블로그 {i+1} 내용:\n{blog}\n")

# 드라이버 종료
driver.quit()