def get_data(large_category,middle_category,small_category,url):

    # 웹 크롤링 동작
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    import time
    from bs4 import BeautifulSoup
    from datetime import datetime

    webdriver_manager_directory = ChromeDriverManager().install()
    browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
    # ChromeDriver 실행
    from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException    # Element : 웹요소 찾지 못할 때 / Window : 창이 없거나 찾을 수 없을 때
    # Chrome WebDriver의 capabilities 속성 사용
    capabilities = browser.capabilities
    # - 정보 획득
    # from selenium.webdriver.support.ui import Select      # Select : dropdown 메뉴 다루는 클래스
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

    # 몽고db 저장
    from pymongo import MongoClient
    # mongodb에 접속
    mongoClient = MongoClient("mongodb://localhost:27017")
    # database 연결
    database = mongoClient["wiggle"]
    # collection 작업
    wiggles = database['product']
    # - 주소 입력

    browser.get(url)


    # 페이지 갯수
    page_count = browser.find_elements(by=By.CSS_SELECTOR, value='#container > div.xans-element-.xans-product.xans-product-normalpaging.ec-base-paginate > ol > li')

    # 다음 페이지
    try:
        next_page_button = browser.find_element(by=By.CSS_SELECTOR, value='#container > div.xans-element-.xans-product.xans-product-normalpaging.ec-base-paginate > a:nth-child(4) > img')
    except:
        pass

    # 아이템 가져오기
    # url = browser.current_url
    # browser.get(url)
    for i in range(len(page_count)):

        page_counter = 1
        time.sleep(1)

        items = browser.find_elements(by=By.CSS_SELECTOR, value='#container > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li')
        time.sleep(1)
        for item in items:
            try:
                get_HTML = item.get_attribute('outerHTML')
                soup = BeautifulSoup(get_HTML, 'html.parser')
                try:
                    # 이미지 추출
                    image = soup.find('img', class_='thumb_img')['src']
                except:
                    image = ''

                try:
                    # 제목 추출
                    title = soup.find('div', class_='name').text.strip()
                except:
                    title = ''

                try:    
                    # 이전 가격 추출
                    old_price = soup.find('div', class_='prs price1').text.strip()
                    old_price = old_price.replace(',','')
                    old_price = old_price.replace('원','')
                except:
                    old_price = ''
                    
                try:    
                    # 현재 가격 추출
                    new_price = soup.find('div', class_='prs price2').text.strip()
                    new_price = new_price.replace(',','')
                    new_price = new_price.replace('원','')
                except:
                    new_price = ''
                
                try:
                    # 할인율 추출
                    discount = soup.find('div', class_='dc_rate rate10').text.strip()
                except:
                    discount = ''

                try:
                    # 리뷰 개수 추출
                    review_count = soup.find('span', class_='snap_review_count').text.strip()
                    review_count = review_count.replace('리뷰 ','')
                except:
                    review_count = ''

                try:
                    soldout = browser.find_element(by=By.CSS_SELECTOR, value="#anchorBoxId_2227 > div > div.ico_soldout > img").get_attribute("src")
                    soldout = True
                except:
                    soldout = False


                # 데이터 저장
                data={
                'large_category' : large_category,
                'middle_category' : middle_category,
                'small_category' : small_category,
                'image_url' : image,
                'title' : title,
                'old_price' : old_price,
                'new_price' : new_price,
                'discount_rate' : discount,
                'review_count' : review_count,
                'isSoldout' : soldout
                }
                wiggles.insert_one(data)

            except:
                pass
        try:
            if page_counter != len(page_count):                                  
                next_page_button.click()
                page_counter += 1
                continue
            break
        except:
            break    
    browser.close()
    