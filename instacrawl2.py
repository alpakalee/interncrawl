import time
from datetime import datetime
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import messagebox

# 기본 키워드 리스트
default_keywords = [
    "웨딩", "결혼", "박람회", "신혼", "돌잔치", "플래너", "팔순", "피로연", 
    "어반브룩", "광주", "남구", "메이크업", "프로필", "강남", "청담", 
    "스튜디오", "협찬"
]

results = []
seen_data = set()
current_index = 0

url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'

###################################################################################################
# 웹드라이버 설정 및 실행
def driversetup(url):
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(3)
    return driver
###################################################################################################

def get_user_input(root):
    user_input = {}

    def on_submit():
        user_input['userid'] = id_entry.get()
        user_input['userpw'] = pw_entry.get()
        user_input['target'] = int(target_entry.get())
        additional_keywords = keywords_entry.get()
        user_input['keywords'] = [keyword.strip() for keyword in additional_keywords.split(",")]
        input_window.destroy()

    input_window = tk.Toplevel(root)
    input_window.title("사용자 입력")

    tk.Label(input_window, text="인스타그램 아이디:").grid(row=0, column=0, pady=5)
    id_entry = tk.Entry(input_window)
    id_entry.grid(row=0, column=1, pady=5)

    tk.Label(input_window, text="인스타그램 비밀번호:").grid(row=1, column=0, pady=5)
    pw_entry = tk.Entry(input_window, show='*')
    pw_entry.grid(row=1, column=1, pady=5)

    tk.Label(input_window, text="수집할 게시글의 수:").grid(row=2, column=0, pady=5)
    target_entry = tk.Entry(input_window)
    target_entry.grid(row=2, column=1, pady=5)

    default_keywords_str = ", ".join(default_keywords)
    tk.Label(input_window, text=f"추가할 키워드를 입력하세요 (쉼표로 구분):\n기본 키워드: [{default_keywords_str}]").grid(row=3, column=0, columnspan=2, pady=5)
    keywords_entry = tk.Entry(input_window)
    keywords_entry.grid(row=4, column=0, columnspan=2, pady=5)

    submit_button = tk.Button(input_window, text="Submit", command=on_submit)
    submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    input_window.transient(root)
    input_window.grab_set()
    root.wait_window(input_window)
    
    return user_input

def login_and_search(userid, userpw, target, additional_keywords):
    driver = driversetup(url)

    id_box = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
    id_box.send_keys(userid)
    pw_box = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
    pw_box.send_keys(userpw)
    pw_box.send_keys(Keys.RETURN)
    time.sleep(12)

    search_box = driver.find_element(By.XPATH, '//*[@aria-label="탐색 탭" and @height="24"]')
    search_box.click()
    time.sleep(7)

    def select_first(driver):
        elements = driver.find_elements(By.CLASS_NAME, '_aagw')
        if len(elements) >= 2:
            second_element = elements[1]
            second_element.click()
            time.sleep(5)
        else:
            print("두 번째 요소를 찾을 수 없습니다.")

    def get_content(driver, keywords, first_click=False):
        global current_index
        try:
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            
            parent_div = driver.find_element(By.CLASS_NAME, '_aaqt')
            a_tag = parent_div.find_element(By.TAG_NAME, 'a')
            target_id = a_tag.text

            hashtags = []
            try:
                parent_divs = soup.find_all("div", class_="_a9zr")
                for parent_div in parent_divs:
                    a_tags = parent_div.find_all("a", href=True)
                    for a_tag in a_tags:
                        if a_tag.get_text().startswith("#"):
                            hashtags.append(a_tag.get_text())
            except Exception as e:
                print(f"Hashtags extraction error: {e}")
                hashtags = []

            try:
                place = soup.select('div._aaqm')[0].text
            except:
                place = ''

            if any(keyword in hashtag for keyword in keywords for hashtag in hashtags):
                if target_id not in seen_data:
                    seen_data.add(target_id)
                    results.append({"Target ID": target_id, "위치": place, "Hashtags": hashtags})

            next_boxes = driver.find_elements(By.XPATH, '//button[contains(@class, "_abl-")]')
            if first_click:
                next_boxes[0].click()        
            else:
                next_boxes[1].click()
            time.sleep(0.4)
        except Exception as e:
            print(f"Error occurred: {e}")
            save_results()
            try:
                exit_boxes = driver.find_elements(By.XPATH, '//*[@aria-label="닫기"]')
                exit_boxes[1].click()
                print("재시작합니다")
            except Exception as close_error:
                print(f"재시작 중 에러가 발생했습니다: {close_error}")
                input("계속하려면 엔터를 누르세요...")
                return False
            return True
        current_index += 1
        return True

    def save_results():
        df = pd.DataFrame(results)
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"instagram_posts_{current_time}.xlsx"
        df.to_excel(file_name, index=False)
        print(f"Results saved to {file_name}")

    keywords = default_keywords + additional_keywords

    select_first(driver)
    get_content(driver, keywords, first_click=True)

    while current_index < target:
        print(f"{current_index + 1}번째 게시글 크롤링 중")
        if not get_content(driver, keywords):
            input("다시 시작하려면 엔터를 누르세요...")
            continue

    save_results()

    driver.quit()

def main():
    root = tk.Tk()
    user_input = get_user_input(root)
    root.withdraw()  # 사용자 입력을 받은 후 창을 숨깁니다.

    if user_input and all(key in user_input for key in ['userid', 'userpw', 'target', 'keywords']):
        login_and_search(user_input['userid'], user_input['userpw'], user_input['target'], user_input['keywords'])
    else:
        messagebox.showerror("Error", "모든 입력을 완료해 주세요.", parent=root)

if __name__ == "__main__":
    main()
