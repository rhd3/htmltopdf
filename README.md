사용법..

1. wkhtmltopdf.exe 파일 위치 설정
path_to_wkhtmltopdf = r"C:\\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

2. 메인 콘텐츠 div 찾기
target_div = soup.find("div", class_="tt_article_useless_p_margin contents_style")
class 부분 변경
