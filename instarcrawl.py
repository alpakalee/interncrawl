import time
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

query = input('검색할 키워드를 입력하세요: ')
userid = input('인스타그램 아이디 : ')
userpw = input('인스타그램 비밀번호 : ')



url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'

###################################################################################################
# 웹드라이버 설정 및 실행
def driversetup(url):
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)
    return driver
###################################################################################################


driver = driversetup(url)
id_box = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
id_box.send_keys(userid)
pw_box = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
pw_box.send_keys(userpw)
pw_box.send_keys(Keys.RETURN)
time.sleep(10)

search_box = driver.find_element(By.XPATH, '//*[@aria-label="검색" and @height="24"]')
search_box.click()
time.sleep(5)

search_key_box = driver.find_element(By.XPATH, '//*[@aria-label="입력 검색"]')
search_key_box.send_keys('#' + query)
time.sleep(5)
search_click_box = driver.find_element(By.CSS_SELECTOR, '.x9f619.x1n2onr6.x1ja2u2z.x78zum5.x1iyjqo2.xs83m0k.xeuugli.x1qughib.x6s0dn4.x1a02dak.x1q0g3np.xdl72j9')
search_click_box.click()
time.sleep(5)

#페이지를 읽어들일 수 없습니다.
page_not_found_box = driver.find_element(By.XPATH, '//*[contains(text(),"페이지 새로 고침")]')
page_not_found_box.click()
time.sleep(5)

def select_first(driver):
    first = driver.find_element(By.CLASS_NAME, '_aagw')
    first.click()
    time.sleep(3)

########################################################################################

def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    parent_div = soup.find("div", class_="_aaqt")
    # 해당 div 밑에 있는 a 태그 찾기
    a_tag = parent_div.find("a", href=True)
    # 텍스트 값 추출
    target_id = a_tag.get_text()
    
    hashtags = []
    try:
        # _a9zr 클래스를 가진 모든 div 요소 찾기
        parent_divs = soup.find_all("div", class_="_a9zr")
        for parent_div in parent_divs:
            a_tags = parent_div.find_all("a", href=True)
            # #해시태그가 붙은 내용 추출
            for a_tag in a_tags:
                if a_tag.get_text().startswith("#"):
                    hashtags.append(a_tag.get_text())
    except:
        hashtags = []

    time_tag = soup.find("time", class_="x1p4m5qa")
    time = time_tag.get_text()

    #좋아요도 나중에 크롤링

    # try:
    #     place = soup.select('div._aaqm')[0].text
    # except:
    #     place = ''
    
    data = [target_id, time, hashtags]
    return data

def move_next(driver):
    right = driver.find_element(By.XPATH, '//button[@class="_abl-"]')
    right.click()
    time.sleep(2)

select_first(driver)

results = []

target = 5
for i in range(target):
    print(f"{i + 1}번째 게시글 크롤링 중")
    post_data = get_content(driver)
    results.append(post_data)
    time.sleep(2)
    move_next(driver)

df = pd.DataFrame(results, columns=["Target ID", "Time", "Hashtags"])

# 파일 이름에 query 변수 값 포함
file_name = f"instagram_posts_{query}.xlsx"

# 엑셀 파일로 저장
df.to_excel(file_name, index=False)

print("Results saved to xlsx")

driver.quit()