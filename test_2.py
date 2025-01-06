file_name = "index.html"
main_text = "<h1>오늘 수업은 여기까지입니다.</h1>"
with open(f"{file_name}", "w", encoding="utf-8") as f:
    f.write(f"{main_text}")