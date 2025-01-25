from parse_doc import PDFParser
from sqliteController import SQLiteManager
from textEmbedding import EmbeddingGenerator
from fileSelector import select_pdf_file
from search import get_most_similar_paragraph
import os
import curses
import locale

# Set locale to support UTF-8
locale.setlocale(locale.LC_ALL, '')
curses.encoding = 'utf-8'


# PDF 파싱 후 데이터베이스에 저장하는 함수
def save_parsed_data_to_db(pdf_parser, embedding_Module:EmbeddingGenerator, db, division):
    """PDF에서 데이터를 파싱하여 SQLite 데이터베이스에 저장합니다."""
    
    dataset = {}

    # 파싱된 개정 데이터 가져오기
    if division == 0:
        dataset = pdf_parser.get_amendments()
    elif division == 1:
        dataset = pdf_parser.get_new_rule()

    # 파싱한 데이터 삽입
    insert_query = "INSERT INTO legal_vectors (vector, division, date, clauses) VALUES (?, ?, ?, ?)"
    
    for date, clauses_list in dataset.items():
        for clause_info in clauses_list:
            clause_text, clause_number, sub_clause_number = clause_info

            vector_data = embedding_Module.generate_embeddings(clause_text)

            # 조항 번호는 xxxyyy 형식으로 결합 (예: 2조의3 -> 200003)
            clause_combined = clause_number * 1000 + sub_clause_number

            # 데이터베이스에 데이터 삽입
            db.insert(insert_query, (vector_data, division, date, clause_combined))

    print("PDF 파싱 데이터가 성공적으로 DB에 저장되었습니다.")
    
    
def mainUI(stdscr):
    curses.curs_set(0)  # 커서를 숨김
    stdscr.clear()
    
    menu_list = ['검색', '종료']
    selected_index = 0
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # 제목 출력
        title = "어떤 파일을 선택하시겠습니까?"
        stdscr.addstr(0, 0, title)

        # 파일 목록 출력
        for idx, menu in enumerate(menu_list):
            if idx == selected_index:
                # 선택된 파일에 "O" 표시
                menu_display = f"{idx + 1}. {menu} O"
                stdscr.addstr(idx + 1, 0, menu_display, curses.A_REVERSE)
            else:
                # 선택되지 않은 파일
                menu_display = f"{idx + 1}. {menu}"
                stdscr.addstr(idx + 1, 0, menu_display)

        # 방향키로 파일 선택
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_index > 0:
            selected_index -= 1
        elif key == curses.KEY_DOWN and selected_index < len(menu_list) - 1:
            selected_index += 1
        elif key == ord('\n'):
            # 엔터키 입력 시 선택 완료
            break
        elif key == ord('q'):
            return menu_list[2]

    # 선택된 파일 반환
    return menu_list[selected_index]    


def search_with_curses(db):
    division = ['개정', '신설']
    def main(stdscr):
        # Clear screen
        stdscr.clear()
        
        # Enable cursor and get user input
        curses.echo()
        stdscr.addstr(0, 0, "Enter the paragraph to search: ")
        # if stdin backspace ^Z, ^D에 대한 처리, 이후 다시 입력 받기
        try:
            query_text = stdscr.getstr(1, 0).decode("utf-8")
        except:
            curses.endwin()
            curses.wrapper(main)
            return
        
        
        # Perform search
        most_similar_paragraph = get_most_similar_paragraph(query_text, db)
        clause = [most_similar_paragraph[0]//1000, most_similar_paragraph[0]%1000]
        
        # Display result
        stdscr.addstr(3, 0, f"검색 결과 : {most_similar_paragraph[1]} {division[most_similar_paragraph[2]]}, {int(clause[0])}조 {int(clause[1])}항")
        stdscr.refresh()
        stdscr.getch()

    curses.wrapper(main)

# main 함수
if __name__ == "__main__":
    while True:
        selected_menu = curses.wrapper(mainUI)
        db = SQLiteManager('example.db')

        if selected_menu == '검색':
            search_with_curses(db)
        elif selected_menu == '삽입':
            # PDF 파일 경로
            pdf_file_path = select_pdf_file('./docs')
            
            embedding_Module = EmbeddingGenerator()
            
            # PDF 파서 객체 생성 및 텍스트 추출
            pdf_parser = PDFParser(pdf_file_path)
            pdf_texts = pdf_parser.extract_text_from_pdf()
            pdf_parser.parse_text(pdf_texts)

            # 데이터베이스 이름

            # PDF 파싱 데이터 저장
            save_parsed_data_to_db(pdf_parser, embedding_Module, db, 0)
            save_parsed_data_to_db(pdf_parser, embedding_Module, db, 1)
        elif selected_menu == '종료':
            break