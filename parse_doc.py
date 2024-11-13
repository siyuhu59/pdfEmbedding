import re
from pdfminer.high_level import extract_text

class PDFParser:
    def __init__(self, pdf_path):
        """초기화 함수로, 파싱할 PDF 파일 경로를 설정합니다."""
        self.pdf_path = pdf_path
        self.amendment_pattern = r"<개정 ((\d{4}\. \d{1,2}\. \d{1,2}\.,?\s?)+)>"
        self.new_rule_pattern = r"<신설 (\d{4}\. \d{1,2}\. \d{1,2}\.)>"
        self.current_pattern = r"제\d+조(?:의\d+)?"
        self.amendments = {}
        self.new_rule = {}
        self.current_clause = [1, 0]  # 현재 조항 번호를 저장하는 리스트

    def extract_text_from_pdf(self):
        """PDF 파일에서 텍스트를 추출합니다."""
        return extract_text(self.pdf_path)

    def parse_text(self, texts):
        """추출한 텍스트에서 개정 정보와 조항 번호를 파싱합니다."""
        for text in texts.split('\n'):
            amendment_match = re.findall(self.amendment_pattern, text)
            new_rule_match = re.findall(self.new_rule_pattern, text)
            current_match = re.findall(self.current_pattern, text)

            # 조항 번호를 추출
            if current_match:
                self.current_clause[0] = int(current_match[0].split('조')[0][1:])
                self.current_clause[1] = int(current_match[0].split('조')[1][1:] if current_match[0].split('조')[1][1:] else 0)

            # 개정 정보를 추출하여 딕셔너리에 저장
            if amendment_match:
                dates = amendment_match[0][0]
                date_list = [date.strip() for date in dates.split(',')]
                for date in date_list:
                    if date not in self.amendments:
                        self.amendments[date] = []
                    self.amendments[date].append([text.split('<')[0], self.current_clause[0], self.current_clause[1]])
                    
        # 신설 정보를 추출하여 딕셔너리에 저장
            if new_rule_match:
                date = new_rule_match[0]
                if date not in self.new_rule:
                    self.new_rule[date] = []
                self.new_rule[date].append([text.split('<')[0], self.current_clause[0], self.current_clause[1]])  # division 1: 신설

    def get_amendments(self):
        return self.amendments

    def get_new_rule(self):
        return self.new_rule

# 사용 예시
if __name__ == "__main__":
    # PDF 파일 경로 설정
    pdf_file_path = './docs/income_tax.pdf'

    # 파서 객체 생성 및 PDF 텍스트 추출
    parser = PDFParser(pdf_file_path)
    pdf_texts = parser.extract_text_from_pdf()

    # 텍스트 파싱
    parser.parse_text(pdf_texts)

    # 개정 정보 출력
    amendments = parser.get_amendments()
    new_rule = parser.get_new_rule()
    print(new_rule)
    print(amendments)
