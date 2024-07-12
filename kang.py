import time
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from bs4 import BeautifulSoup
import pandas as pd
userid = "00smun@naver.com"
userpw = "rkdtjdans1"
# url = "https://timetreeapp.com/calendars/draFTMQN43BJ"  # 시험용
memo_dic = {}
url = "https://timetreeapp.com/calendars/EY13JGM4xNU1"  # 어반브룩1
# url = "https://timetreeapp.com/calendars/uUQNENH6rNp7"# 어반브룩2
###################################################################################################
# 웹드라이버 설정 및 실행
def driversetup(url):
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )
    driver.get(url)
    time.sleep(5)
    return driver
###################################################################################################
driver = driversetup(url)
id_box = driver.find_element(
    By.XPATH,
    '//*[@id="react-root"]/div/div[1]/div[2]/div/div[2]/form/div[1]/div[1]/div/input',
)
id_box.send_keys(userid)
pw_box = driver.find_element(
    By.XPATH,
    '//*[@id="react-root"]/div/div[1]/div[2]/div/div[2]/form/div[1]/div[2]/div/input',
)
pw_box.send_keys(userpw)
pw_box.send_keys(Keys.RETURN)
time.sleep(5)
try:
    # # 현재 달을 2024년 1월로 맞추기
    target_month = "2024-01"
    current_month_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "time.css-1vvhl73.e1ik4xi10"))
    )
    current_month = current_month_element.get_attribute("datetime")
    while current_month != target_month:
        prev_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.ttfont-arrow_left.css-1bh8r2g.e1vzq5cj0")
            )
        )
        prev_button.click()
        time.sleep(1)  # 이전 달 페이지 로드 대기
        current_month_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "time.css-1vvhl73.e1ik4xi10")
            )
        )
        current_month = current_month_element.get_attribute("datetime")
    print("start")
    # 2024년 1월부터 12월까지 반복
    for month in range(1, 13):
        print(month, "월")
        # 현재 페이지에서 작업 수행
        plus_buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.eventsCount.css-lnyvlk.e1xwep1t0")
            )
        )
        print(len(plus_buttons))
        for plus in plus_buttons:
            plus.click()
            print(2)
            # 특정 범위 내의 span 요소들 선택 (예: 특정 div 내의 span 요소들)
            parent_class = "css-a3g8ak.ea5oywd5"
            # css-a3g8ak ea5oywd5
            # child_class = "css-13avop6.e101a0a20"
            child_class = "css-1a8b0li.e4ilutn1"
            parent_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, parent_class))
            )
            # 상위 요소 내에서 자식 요소를 찾습니다.
            span_elements_within_div = parent_element.find_elements(
                By.CLASS_NAME, child_class
            )
            # print(len(span_elements_within_div))
            for span_element in span_elements_within_div:
                span_element.click()
                try:
                    name_element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "h2.title"))
                    )
                    linkify_element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "span.Linkify")
                        )
                    )
                    date_element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(
                            # (By.CSS_SELECTOR, "div.css-u70ddh.efsuzcs0")
                            (By.CSS_SELECTOR, "div.css-3qua7i.eq8i85q2")
                        )
                    )
                    print(date_element.text)
                    memo_dic[name_element.text] = [
                        date_element.text,
                        linkify_element.text,
                    ]
                except:
                    print("Linkify element not found after clicking span button")
                driver.back()
            click = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.weekday.isSunday")
                )
            )
            click.click()
            time.sleep(0.5)
        #
        # span_buttons = WebDriverWait(driver, 20).until(
        #     EC.presence_of_all_elements_located(
        #         # (By.CSS_SELECTOR, "div.css-qzyr6w.e4ilutn3")
        #         (By.CSS_SELECTOR, "span.css-1a8b0li.e4ilutn1")
        #     )
        # )
        # for span_button in span_buttons:
        #     span_button.click()
        #     try:
        #         # Linkify 요소가 나타날 때까지 대기
        #         name_element = WebDriverWait(driver, 20).until(
        #             EC.presence_of_element_located((By.CSS_SELECTOR, "h2.title"))
        #         )
        #         linkify_element = WebDriverWait(driver, 20).until(
        #             EC.presence_of_element_located((By.CSS_SELECTOR, "span.Linkify"))
        #         )
        #         date_element = WebDriverWait(driver, 20).until(
        #             EC.presence_of_element_located(
        #                 (By.CSS_SELECTOR, "div.css-3qua7i.eq8i85q2")
        #             )
        #         )
        #         memo_dic[name_element.text] = [date_element.text, linkify_element.text]
        #     except:
        #         print(span_button.text)
        #     time.sleep(1)  # 잠시 대기
        #     # "다음 달" 버튼 클릭
        #
        if month < 12:  # 12월 이후에는 클릭하지 않음
            next_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "span.ttfont-arrow_right.css-1bh8r2g.e1vzq5cj0",
                    )
                )
            )
            next_button.click()
        time.sleep(1)  # 다음 달 페이지 로드 대기
finally:
    # 브라우저 닫기
    driver.quit()
    print(memo_dic)
memo = pd.DataFrame(memo_dic)
memo = memo.T
memo.to_csv("memo_plus.csv")
memo.head()