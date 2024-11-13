import os
import curses

class FileSelectorUI:
    def __init__(self, directory):
        """지정된 디렉토리에서 PDF 파일 목록을 가져옵니다."""
        self.directory = directory
        self.files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
        self.selected_index = 0

    def display_menu(self, stdscr):
        """파일 선택 UI를 표시합니다."""
        curses.curs_set(0)  # 커서를 숨김
        stdscr.clear()
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            # 제목 출력
            title = "어떤 파일을 선택하시겠습니까?"
            stdscr.addstr(0, 0, title)

            # 파일 목록 출력
            for idx, file_name in enumerate(self.files):
                if idx == self.selected_index:
                    # 선택된 파일에 "O" 표시
                    file_name_display = f"{idx + 1}. {file_name} O"
                    stdscr.addstr(idx + 1, 0, file_name_display, curses.A_REVERSE)
                else:
                    # 선택되지 않은 파일
                    file_name_display = f"{idx + 1}. {file_name}"
                    stdscr.addstr(idx + 1, 0, file_name_display)

            # 방향키로 파일 선택
            key = stdscr.getch()

            if key == curses.KEY_UP and self.selected_index > 0:
                self.selected_index -= 1
            elif key == curses.KEY_DOWN and self.selected_index < len(self.files) - 1:
                self.selected_index += 1
            elif key == ord('\n'):
                # 엔터키 입력 시 선택 완료
                break

        # 선택된 파일 반환
        return self.files[self.selected_index]

def select_pdf_file(directory='./docs'):
    """CLI 파일 선택 메뉴 실행."""
    file_selector = FileSelectorUI(directory)
    selected_file = curses.wrapper(file_selector.display_menu)
    selected_file = f'{directory}/{selected_file}'
    return selected_file

# 예시 사용
if __name__ == "__main__":
    directory = './docs'  # PDF 파일이 저장된 디렉토리
    selected_file = select_pdf_file(directory)
    print(f"선택된 파일: {selected_file}")
