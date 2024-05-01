# 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

from datetime import datetime
from bs4 import BeautifulSoup


webdriver_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
# ChromeDriver 실행
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException    # Element : 웹요소 찾지 못할 때 / Window : 창이 없거나 찾을 수 없을 때
# Chrome WebDriver의 capabilities 속성 사용
capabilities = browser.capabilities
from selenium.webdriver.common.by import By
# - 정보 획득
# from selenium.webdriver.support.ui import Select      # Select : dropdown 메뉴 다루는 클래스
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# 몽고db 저장
from pymongo import MongoClient
# mongodb에 접속
mongoClient = MongoClient("mongodb://localhost:27017")
# database 연결
database = mongoClient["wiggle"]
# collection 작업
wiggles = database['qna']
# - 주소 입력

browser.get("https://wiggle-wiggle.com/board/product/list.html?board_no=6&page=1")


while True:

    time.sleep(2)

    page_nation_value = "#container > div.xans-element-.xans-board.xans-board-paging-4.xans-board-paging.xans-board-4.ec-base-paginate.snapreview_hidden > a:nth-child(3) > img"
    next_page_button = browser.find_element(by=By.CSS_SELECTOR, value=page_nation_value)


    time.sleep(1)


    contents_bundle = browser.find_elements(by=By.CSS_SELECTOR, value='#container > div.xans-element-.xans-board.xans-board-listpackage-4.xans-board-listpackage.xans-board-4 > div.ec-base-table.typeList.gBorder.snapreview_hidden > table > tbody >tr')

    time.sleep(1)


    for content in contents_bundle:

        # 인덱스 번호
        try:
            index_num = content.find_element(by=By.CSS_SELECTOR, value='td:nth-child(1)').text
        except:
            index_num = ''
        
        # 상품 주소
        try:
            product_href = content.find_element(by=By.CSS_SELECTOR, value="td.thumb.left > a").get_attribute("href")
        except:
            product_href = ''

        # 상품 이름
        try:
            get_HTML = content.get_attribute('outerHTML')
            soup = BeautifulSoup(get_HTML, 'html.parser')
            span_text = soup.find('span').text.strip()
            product_name = span_text
            pass
        except:
            product_name = ''
            pass

        # 문의 종류
        try:
            category = content.find_element(by=By.CSS_SELECTOR, value='td.subject.left.txtBreak > a').text
        except:
            category = ''

        # 문의자
        try:
            customer_name = content.find_element(by=By.CSS_SELECTOR, value='td:nth-child(5)').text
        except:
            customer_name = ''

        # 문의 날짜
        try:
            date = content.find_element(by=By.CSS_SELECTOR, value='td:nth-child(6) > span').text
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        except:
            date = ''

        # 데이터 저장
        data={
        'index_num' : index_num,
        'product_href' : product_href,
        'product_name' : product_name,
        'category' : category,
        'customer_name' : customer_name,
        'date' : date,
        }
        wiggles.insert_one(data)

    if index_num == 1:
        break

    try:
        next_page_button.click()
    except:
        break

browser.close()
