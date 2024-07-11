import time #sleep을 위해 필요
from datetime import datetime #엑셀파일 저장시 시간기록
from selenium.webdriver import ChromeOptions #크롬 옵션
from selenium import webdriver #웹 열기
from selenium.webdriver.common.by import By # 객체 찾기
from selenium.webdriver.common.keys import Keys # 객체에 입력
from selenium.webdriver.chrome.service import Service as ChromeService #크롬으로 열기
from bs4 import BeautifulSoup #크롤링
import pandas as pd #데이터 정리
import tkinter as tk # GUI
from tkinter import messagebox #GUI 입력시 에러창

results = [] #데이터 결과
seen_data = set() #중복제거
current_index = 0 #현재 크롤링 중인 게시물 위치

url = 'https://www.instagram.com/accounts/login/?source=auth_switcher' # 첫 시작 위치

###################################################################################################
# 웹드라이버 설정 및 실행
def driversetup(url):
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    
    # 로컬에 저장된 ChromeDriver 경로를 지정
    driver_path = "./chromedriver.exe"  # chromedriver.exe 파일이 스크립트와 동일한 디렉토리에 존재.
    driver = webdriver.Chrome(service=ChromeService(driver_path), options=options)
    driver.get(url)
    time.sleep(3)
    return driver
###################################################################################################

def get_user_input(): # GUI 상에서 사용자의 입력을 받아오기
    user_input = {}

    def on_submit(): #SUBMIT을 눌렀을때 사용자의 입력을 가져오기
        user_input['userid'] = id_entry.get()
        user_input['userpw'] = pw_entry.get()
        try:
            user_input['target'] = int(target_entry.get())
        except ValueError:
            messagebox.showerror("Error", "수집할 게시글의 수는 숫자여야 합니다.")
            return

        user_keywords = keywords_entry.get()
        user_input['keywords'] = [keyword.strip() for keyword in user_keywords.split(",") if keyword.strip()]
        root.quit()

    root = tk.Tk() #GUI 생성하기
    root.title("사용자 입력")
    root.geometry("760x230")  # 창 크기 고정

    tk.Label(root, text="인스타그램 아이디:", padx=10).grid(row=0, column=0, pady=5, sticky='w')
    id_entry = tk.Entry(root, width=40)
    id_entry.grid(row=0, column=1, pady=5, sticky='w', padx=10)

    tk.Label(root, text="인스타그램 비밀번호:", padx=10).grid(row=1, column=0, pady=5, sticky='w')
    pw_entry = tk.Entry(root, show='*', width=40)
    pw_entry.grid(row=1, column=1, pady=5, sticky='w', padx=10)

    tk.Label(root, text="수집할 게시글의 수:", padx=10).grid(row=2, column=0, pady=5, sticky='w')
    target_entry = tk.Entry(root, width=40)
    target_entry.grid(row=2, column=1, pady=5, sticky='w', padx=10)

    tk.Label(root, text="키워드를 입력하세요 (쉼표로 구분) ex) 웨딩,결혼,박람회", padx=10).grid(row=3, column=0, pady=5, sticky='w')
    keywords_entry = tk.Entry(root, width=100)
    keywords_entry.grid(row=4, column=0, columnspan=2, pady=5, padx=10)

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    root.mainloop() # GUI 창 유지시키기
    
    return user_input

def login_and_search(userid, userpw, target, user_keywords): # 로그인 및 크롤링
    driver = driversetup(url) # 크롬 드라이버 실행


    # 로그인 
    id_box = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
    id_box.send_keys(userid)
    pw_box = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
    pw_box.send_keys(userpw)
    pw_box.send_keys(Keys.RETURN)
    time.sleep(12)

    # 탐색 탭으로 이동
    search_box = driver.find_element(By.XPATH, '//*[@aria-label="탐색 탭" and @height="24"]')
    search_box.click()
    time.sleep(7)

    # 탐색 탭의 첫 게시물을 찾아서 클릭
    def select_first(driver):
        elements = driver.find_elements(By.CLASS_NAME, '_aagw')
        if len(elements) >= 2:
            second_element = elements[1]
            second_element.click()
            time.sleep(5)
        else:
            print("크롤링을 시작할 첫 게시물을 찾지 못했습니다.")

    # 크롤링 시작
    def get_content(driver, keywords, first_click=False):
        global current_index
        try:
            # 페이지를 BeautifulSoup으로 파싱
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            
            # id 추출
            parent_div = driver.find_element(By.CLASS_NAME, '_aaqt')
            a_tag = parent_div.find_element(By.TAG_NAME, 'a')
            target_id = a_tag.text

            # 해시태그 추출
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

            # 장소 추출
            try:
                place = soup.select('div._aaqm')[0].text
            except:
                place = ''

            if not keywords or any(keyword in hashtag for keyword in keywords for hashtag in hashtags):
                if target_id not in seen_data:
                    seen_data.add(target_id)
                    results.append({"Target ID": target_id, "위치": place, "Hashtags": hashtags})

            next_boxes = driver.find_elements(By.XPATH, '//button[contains(@class, "_abl-")]')

            # 첫 게시물 일때
            if first_click:
                next_boxes[0].click()        
            else:
                next_boxes[1].click()
            time.sleep(0.4)

        except Exception as e: # 로딩시간에 의해 옆으로 가는 버튼 말고 공유 버튼이 눌러진 경우
            print(f"Error occurred: {e}")
            save_results()
            try: # 공유 창을 닫기
                exit_boxes = driver.find_elements(By.XPATH, '//*[@aria-label="닫기"]')
                exit_boxes[1].click()
                print("재시작합니다")
            except Exception as close_error: # 그래도 오류 발생할 경우
                print(f"재시작 중 에러가 발생했습니다: {close_error}")
                return False
            return True
        current_index += 1
        return True

    def save_results(): # 결과 엑셀로 저장
        df = pd.DataFrame(results)
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"instagram_posts_{current_time}.xlsx"
        df.to_excel(file_name, index=False)
        print(f"Results saved to {file_name}")

    # 키워드 변환(입력이 없는 경우 모든 게시물 크롤링)
    keywords = user_keywords if user_keywords else None


    select_first(driver)
    get_content(driver, keywords, first_click=True)

    while current_index < target: # 지정한 게시물의 갯수가 될 때 까지 반복
        print(f"{current_index + 1}번째 게시글 크롤링 중")
        if not get_content(driver, keywords):
            input("다시 시작하려면 엔터를 누르세요...")
            continue

    save_results()

    driver.quit()

def main(): #메인 함수
    user_input = get_user_input()

    if user_input and all(key in user_input for key in ['userid', 'userpw', 'target']):
        login_and_search(user_input['userid'], user_input['userpw'], user_input['target'], user_input['keywords'])
    else:
        messagebox.showerror("Error", "모든 입력을 완료해 주세요.")

if __name__ == "__main__": # 프로그램 실행
    main()
