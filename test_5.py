from datetime import datetime
now = datetime.now() # 현재 날짜와 시간을 가져오기
today = f"{now.year}년 {now.month}월 {now.day}일" # 날짜를 문자열로 변환하기

file_name = "index.html"
title_text = "쿠팡 스크래핑"
main_text = "<p>쿠팡 스크래핑한 결과가 들어갑니다.</p>"
html_text = f"""<!DOCTYPE HTML>
<html>
	<head>
		<title>Generic Page - Massively by HTML5 UP</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="assets/css/main.css" />
		<noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>
	</head>
	<body class="is-preload">

		<!-- Wrapper -->
			<div id="wrapper">
				<!-- Header -->
					<header id="header">
						<a href="index.html" class="logo">Massively</a>
					</header>
				<!-- Main -->
					<div id="main">
						<!-- Post -->
							<section class="post">
								<header class="major">
									<span class="date">{today}</span>
									<h1>{title_text}</h1>
									<p>Aenean ornare velit lacus varius enim ullamcorper proin aliquam<br />
									facilisis ante sed etiam magna interdum congue. Lorem ipsum dolor<br />
									amet nullam sed etiam veroeros.</p>
								</header>
								<div class="image main"><img src="images/pic01.jpg" alt="" /></div>
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