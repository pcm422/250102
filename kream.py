from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By # 클래스, 아이디를 css_selector를 이용하여 원하는 값을 가져오기 위한 패키지
from selenium.webdriver.common.keys import Keys # 키보드 입력을 위한 패키지
import pymysql

header_user = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36" # user-agent 설정

options_ = Options() # 옵션 설정
options_.add_argument(f'user-agent={header_user}') # user-agent 설정
options_.add_experimental_option('detach', True) # 브라우저 자동으로 종료되지 않게 스크립트 실행
options_.add_experimental_option('excludeSwitches', ['enable-logging']) # 로그 끄기

driver = webdriver.Chrome(options=options_) # 드라이버 설정

url = "https://kream.co.kr/"
driver.get(url) # url 열기
driver.find_element(By.CSS_SELECTOR, '.btn_search.header-search-button.search-button-margin').click() # 검색창 클릭
driver.find_element(By.CSS_SELECTOR, '.input_search.show_placeholder_on_focus').send_keys('슈프림') # 검색어 입력
driver.find_element(By.CSS_SELECTOR, '.input_search.show_placeholder_on_focus').send_keys(Keys.ENTER) # 엔터키 입력

for i in range(20):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN) # 페이지 다운
    time.sleep(0.5) # 스크롤 후 잠시 대기

html = driver.page_source # 페이지 소스 가져오기
soup = BeautifulSoup(html, 'html.parser') 
items = soup.select('.item_inner')

product_list = []

for item in items:
    product_name = item.select_one('.translated_name').text
    if '후드' in product_name:
        #카테고리
        category = "상의"
        print(f"카테고리 : {category}")
        #브랜드
        brand = item.select_one(".product_info_brand.brand").text
        print(f"브랜드 : {brand}")
        #제품명
        print(f"제품명 : {product_name}")
        #가격
        price = item.select_one(".amount").text
        print(f"가격 : {price}")
        
        product = [category, brand, product_name, price]
        product_list.append(product)
        
        
        print('---------------------------------------------------')
        
driver.quit() # 브라우저 종료

# MySQL 데이터베이스 연결
connection = pymysql.connect(
    host='localhost',       # 데이터베이스 호스트
    user='root',   # 데이터베이스 사용자 이름
    password='990924',# 데이터베이스 비밀번호
    db='kream',    # 사용할 데이터베이스 이름
    charset='utf8mb4'       # 문자 인코딩
)

def execute_query(connection, query, args=None):
    with connection.cursor() as cursor:
        cursor.execute(query, args)
        if query.strip().upper().startswith('SELECT'):
            return cursor.fetchall()
        else:
            connection.commit()

for i in product_list:
    execute_query(connection, "INSERT INTO kream (category, brand, product_name, price) VALUES (%s, %s, %s, %s)", (i[0], i[1], i[2], i[3]))
    
# 데이터베이스 연결 종료
connection.close()