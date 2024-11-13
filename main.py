from parse_doc import PDFParser
from sqliteController import SQLiteManager
from textEmbedding import EmbeddingGenerator
from fileSelector import select_pdf_file

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


# main 함수
if __name__ == "__main__":
    # PDF 파일 경로
    pdf_file_path = select_pdf_file('./docs')
    
    embedding_Module = EmbeddingGenerator()
    
    # PDF 파서 객체 생성 및 텍스트 추출
    pdf_parser = PDFParser(pdf_file_path)
    pdf_texts = pdf_parser.extract_text_from_pdf()
    pdf_parser.parse_text(pdf_texts)

    # 데이터베이스 이름
    db = SQLiteManager('example.db')

    # PDF 파싱 데이터 저장
    save_parsed_data_to_db(pdf_parser, embedding_Module, db, 0)
    save_parsed_data_to_db(pdf_parser, embedding_Module, db, 1)
