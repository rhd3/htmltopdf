import requests
from bs4 import BeautifulSoup
import pdfkit

def extract_div_and_save_pdf():
    try:
        # wkhtmltopdf 경로 설정
        path_to_wkhtmltopdf = r"C:\\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

        # 사용자에게 URL 입력받기
        url = input("웹페이지 URL을 입력하세요: ").strip()

        # 웹페이지 가져오기
        response = requests.get(url)
        response.raise_for_status()
        
        # HTML 파싱
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 특정 div 태그 찾기
        target_div = soup.find("div", class_="tt_article_useless_p_margin contents_style")
        
        if target_div:
            # CSS 추가: 한글 폰트 적용
            css = """
            <style>
                @font-face {
                    font-family: "Malgun Gothic";
                    src: local("Malgun Gothic"), url("C:/Windows/Fonts/malgun.ttf");
                }
                body {
                    font-family: "Malgun Gothic", sans-serif;
                }
            </style>
            """
            content_with_css = f"{css}{str(target_div)}"

            # 추출한 div를 임시 HTML 파일로 저장
            temp_html = "temp_div.html"
            with open(temp_html, "w", encoding="utf-8") as file:
                file.write(content_with_css)

            # wkhtmltopdf 옵션 설정
            options = {
                'encoding': 'utf-8',
                'enable-local-file-access': None,  # HTTPS 처리 옵션
            }
            
            # HTML 파일을 PDF로 변환
            output_pdf = "output.pdf"
            pdfkit.from_file(temp_html, output_pdf, configuration=config, options=options)
            print(f"PDF 파일이 저장되었습니다: {output_pdf}")
        else:
            print("지정된 div 태그를 찾을 수 없습니다.")
    
    except requests.exceptions.RequestException as e:
        print(f"웹페이지를 가져오는 데 실패했습니다: {e}")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

# 스크립트 실행
if __name__ == "__main__":
    extract_div_and_save_pdf()
