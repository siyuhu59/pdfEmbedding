from parse_doc import PDFParser
from textEmbedding import EmbeddingGenerator

def pdfParse(file_path):
    pdf_parser = PDFParser(file_path)
    pdf_texts = pdf_parser.extract_text_from_pdf()
    pdf_parser.parse_text(pdf_texts)
    
    return pdf_parser

def create_table(db, file_name):
    db.create_table(f"""
    CREATE TABLE IF NOT EXISTS '{file_name}' (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 고유 식별자
        vector BLOB NOT NULL,                  -- 문장 또는 문단의 벡터 변환 값
        division INTEGER NOT NULL,             -- 개정(0) 또는 신설(1)을 구분하는 값
        date TEXT NOT NULL,                    -- 개정 또는 신설 날짜 (문자열 형식)
        clauses INTEGER NOT NULL,               -- 조항 번호 (xxxyyy 형식)
        particle TEXT                          -- 글 내 조사 목록
    );
    """)
    
def save_parsed_data_to_db(pdf_parser, table_name, db, division):
    """PDF에서 데이터를 파싱하여 SQLite 데이터베이스에 저장합니다."""
    embedding_Module = EmbeddingGenerator()
    dataset = {}

    # 파싱된 개정 데이터 가져오기
    if division == 0:
        dataset = pdf_parser.get_amendments()
    elif division == 1:
        dataset = pdf_parser.get_new_rule()

    # 파싱한 데이터 삽입
    insert_query = f"INSERT INTO {table_name} (vector, division, date, clauses) VALUES (?, ?, ?, ?)"
    
    for date, clauses_list in dataset.items():
        for clause_info in clauses_list:
            clause_text, clause_number, sub_clause_number = clause_info

            vector_data = embedding_Module.generate_embeddings(clause_text)

            # 조항 번호는 xxxyyy 형식으로 결합 (예: 2조의3 -> 200003)
            clause_combined = clause_number * 1000 + sub_clause_number

            # 데이터베이스에 데이터 삽입
            db.insert(insert_query, (vector_data, division, date, clause_combined))

    print("PDF 파싱 데이터가 성공적으로 DB에 저장되었습니다.")