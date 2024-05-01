# 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
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
wiggles = database['photo_review']
# - 주소 입력


break_counter = 0

while True:
    browser.get("https://wiggle-wiggle.com/board/product/list.html?board_no=4#snapreview_widget1001_0_page=1")
    time.sleep(2)

    # 프레임으로 전환
    frame_element = browser.find_element(by=By.CSS_SELECTOR, value="#review_widget1001_0")  # 프레임 요소 찾기
    browser.switch_to.frame(frame_element)  # 프레임으로 전환

    time.sleep(1)

    page_nation_value = "#pagination>li:nth-child(13)"
    next_page_button = browser.find_element(by=By.CSS_SELECTOR, value=page_nation_value)


    contents_bundle = browser.find_elements(by=By.CSS_SELECTOR, value='#snapreview_contents > div > div.sf_review_item_list > ul > li')

    for content in contents_bundle:
        # 상품 이름
        try:
            item_name = content.find_element(by=By.CSS_SELECTOR, value='div.sf_review_item_detail_info > div > div.sf_review_item_name_and_rating > span').text
        except:
            item_name = ''
        
        # 상품 링크
        try:
            image_src = content.find_element(by=By.CSS_SELECTOR, value="div.sf_review_item_detail_info > div > div.sf_review_sub_img_area > img").get_attribute("src")
        except:
            image_src = ''

        # 평점
        try:
            ratings = content.find_element(by=By.CSS_SELECTOR, value='div.sf_review_item_detail_info > div > div.sf_review_item_name_and_rating > div > div.sf_review_item_rating > span.value.pin_custom_font_color').text
        except:
            ratings = ''

        # 상품평
        try:
            content_text = content.find_element(by=By.CSS_SELECTOR, value='div.sf_review_item_review_list > div.sf_review_item_review.sf_text_overflow > span > span').text
        except:
            content_text = ''

        # 구매자
        try:
            customer_name = content.find_element(by=By.CSS_SELECTOR, value='div.sf_review_item_review_list > div.sf_review_user_data > div.sf_review_user_writer_name > span').text
        except:
            customer_name = ''

        # 총 리뷰 갯수
        try:
            review_count = content.find_element(by=By.CSS_SELECTOR, value='div.sf_review_item_detail_info > div > div.sf_review_item_name_and_rating > div > div.sf_review_item_review_count > span.value.pin_custom_font_color').text
        except:
            review_count = ''

        # 데이터 저장
        data={
        'item_name' : item_name,
        'image_src' : image_src,
        'ratings' : ratings,
        'content_text' : content_text,
        'customer_name' : customer_name,
        'review_count' : review_count,
        }
        wiggles.insert_one(data)

    break_counter += 1
    time.sleep(1)
    
    try:
        next_page_button.click()
    except:
        break

    if break_counter >= 1000:
        break


browser.close()
