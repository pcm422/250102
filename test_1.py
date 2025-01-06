# index.html이라는 파일을 만드는 코드
file_name = "index.html"
with open(f"{file_name}", "w", encoding="utf-8") as f:
    f.write("<h1>오늘 수업은 여기까지입니다.</h1>")