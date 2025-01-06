from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By # 클래스, 아이디를 css_selector를 이용하여 원하는 값을 가져오기 위한 패키지
from selenium.webdriver.common.keys import Keys # 키보드 입력을 위한 패키지

import ftplib

header_user = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36" # user-agent 설정

options_ = Options() # 옵션 설정
options_.add_argument(f'user-agent={header_user}') # user-agent 설정
options_.add_experimental_option('detach', True) # 브라우저 자동으로 종료되지 않게 스크립트 실행
options_.add_experimental_option('excludeSwitches', ['enable-logging']) # 로그 끄기

driver = webdriver.Chrome(options=options_) # 드라이버 설정
keyword = input("검색할 상품 : ")
url = f"https://www.coupang.com/np/search?component=&q={keyword}"

driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

items = soup.select("[class=search-product]")
rank = 1
main_text = ""

# 검색 순위 1위부터 10위까지만 나오게하고 광고 제품은 제외
# 1. 광고 제품인지 아닌지를 구분
# 2. 출력 결과에서 1위부터 10까지만을 출력하도록 조건을 만든다
# 순위?? html 코드에서 추출도 가능하겠지만, 변수 또는 enumerate 사용할 수 있다고 배웠다
for i in items:
    ad = i.select_one(".ad-badge-text")
    
    if not ad:
        product_name = i.select_one(".name").text # 상품명 추출
        product_price = i.select_one(".price-value").text # 가격 추출
        link = f"https://www.coupang.com{i.a['href']}" # 링크 추출
        img = f"https:{i.img['src']}".replace("230x230ex", "400x400ex")
        if i.select_one(".badge.rocket"):
            roket = "로켓배송"  # 로켓배송 여부 확인
        else:
            roket = "일반배송"  # 일반배송 여부 확인
        
        # 결과 출력
        print(f"순위 : {rank}위")
        print(f"제품명 : {product_name}")
        print(f"가격 : {product_price}원")
        print(f"링크 : {link}")
        print(f"이미지 URL : {img}")
        print(f"배송 유형 : {roket}")
        print('---------------------------------------------------')
        main_text = main_text + f"<a href='{link}' target='_blank'><div class='image main'><img src='{img}' alt='image'/></div><h2>{rank}위 {product_name}<h2><b>가격 : {product_price}원</b></a>"
        if rank >= 10:
            break
        rank += 1 # 순위 증가
        
driver.quit()

now = datetime.now() # 현재 날짜와 시간을 가져오기
today = f"{now.year}년 {now.month}월 {now.day}일" # 날짜를 문자열로 변환하기

file_name = "index.html"
title_text = f"오늘의 {keyword}"
summary_text = f"{today} 오늘의 {keyword} 인기상품 top10"
html_text = f"""<!DOCTYPE HTML>
<html>
	<head>
		<title>{title_text}</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="assets/css/main.css" />
		<noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>
	</head>
	<body class="is-preload">

		<!-- Wrapper -->
			<div id="wrapper">
				<!-- Main -->
					<div id="main">
						<!-- Post -->
							<section class="post">
								<header class="major">
									<span class="date">{today}</span>
									<h1>{title_text}</h1>
									<p>{summary_text}</p>
								</header>
                                {main_text}
								</section>
					</div>
			</div>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrollex.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/browser.min.js"></script>
			<script src="assets/js/breakpoints.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>

	</body>
</html>"""
with open(f"{file_name}", "w", encoding="utf-8") as f:
    f.write(f"{html_text}")
    
ftp_url = "pcm0422.dothome.co.kr"
ftp_id = "pcm0422"
ftp_pw = "Fortissimo1!"  # 비밀번호를 직접 입력하지 않도록 주의하세요.
file_to_upload = file_name

ftp = ftplib.FTP()
ftp.connect(ftp_url, 21)
ftp.login(ftp_id, ftp_pw)
ftp.cwd("./html")
my_file = open(f"{file_name}", 'rb')
ftp.storlines(f'STOR {file_name}', my_file)
my_file.close()
ftp.quit()