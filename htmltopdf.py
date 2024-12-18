import os
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import pdfkit

class PDFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Tag to PDF Converter")
        self.wkhtmltopdf_path = self.find_wkhtmltopdf()

        # GUI 요소 배치
        self.setup_gui()
        
    def setup_gui(self):
        # URL 입력
        tk.Label(self.root, text="웹페이지 URL:").grid(row=0, column=0, sticky="w")
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2)

        # 태그 입력
        tk.Label(self.root, text="HTML 태그 (예: div.class):").grid(row=1, column=0, sticky="w")
        self.tag_entry = tk.Entry(self.root, width=50)
        self.tag_entry.grid(row=1, column=1, columnspan=2)

        # PDF 파일명 입력
        tk.Label(self.root, text="PDF 파일명:").grid(row=2, column=0, sticky="w")
        self.pdf_name_entry = tk.Entry(self.root, width=50)
        self.pdf_name_entry.grid(row=2, column=1, columnspan=2)

        # wkhtmltopdf 경로 설정
        tk.Button(self.root, text="wkhtmltopdf 경로 설정", command=self.set_wkhtmltopdf_path).grid(row=3, column=0)
        self.path_label = tk.Label(self.root, text=self.wkhtmltopdf_path or "경로를 찾지 못했습니다.")
        self.path_label.grid(row=3, column=1, columnspan=2)

        # 시작 버튼
        tk.Button(self.root, text="PDF 생성", command=self.convert_to_pdf).grid(row=4, column=0, columnspan=3)

        # 로그 표시
        tk.Label(self.root, text="로그:").grid(row=5, column=0, sticky="w")
        self.log_text = tk.Text(self.root, height=10, width=60)
        self.log_text.grid(row=6, column=0, columnspan=3)

    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

    def find_wkhtmltopdf(self):
        # 자동으로 wkhtmltopdf 경로 찾기
        possible_paths = [
            r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
            r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return ""

    def set_wkhtmltopdf_path(self):
        # 파일 탐색기로 wkhtmltopdf 경로 설정
        path = filedialog.askopenfilename(title="wkhtmltopdf 경로 선택", filetypes=[("Executable Files", "*.exe")])
        if path:
            self.wkhtmltopdf_path = path
            self.path_label.config(text=path)
            self.log(f"wkhtmltopdf 경로 설정: {path}")

    def convert_to_pdf(self):
        # 입력값 확인
        url = self.url_entry.get().strip()
        tag_input = self.tag_entry.get().strip()
        pdf_name = self.pdf_name_entry.get().strip() or "output.pdf"

        if not url or not tag_input or not self.wkhtmltopdf_path:
            messagebox.showerror("오류", "URL, 태그, wkhtmltopdf 경로를 확인해주세요.")
            return

        try:
            # HTML 가져오기
            self.log(f"웹페이지 가져오는 중: {url}")
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # 태그 찾기
            tag, _, class_name = tag_input.partition(".")
            target = soup.find(tag, class_=class_name) if class_name else soup.find(tag)

            if not target:
                self.log("지정된 태그를 찾을 수 없습니다.")
                messagebox.showerror("오류", "지정된 태그를 찾을 수 없습니다.")
                return

            # HTML 생성
            temp_html = "temp.html"
            with open(temp_html, "w", encoding="utf-8") as file:
                file.write(f"<html><body>{str(target)}</body></html>")

            # PDF 생성
            config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path)
            pdfkit.from_file(temp_html, pdf_name, configuration=config)
            self.log(f"PDF 저장 완료: {pdf_name}")
            messagebox.showinfo("성공", f"PDF 파일이 저장되었습니다: {pdf_name}")

        except Exception as e:
            self.log(f"오류 발생: {str(e)}")
            messagebox.showerror("오류", f"오류 발생: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConverterApp(root)
    root.mainloop()
