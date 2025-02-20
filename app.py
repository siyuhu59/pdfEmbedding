from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from sqliteController import SQLiteManager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from search import get_most_similar_paragraph
from utils.generate_id import generate_id
from utils.db_tables import get_tables
from utils.insertData import create_table, pdfParse, save_parsed_data_to_db

app = FastAPI()

# cors 설정
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

DATABASE = "example.db"
FILE_DIRECTORY = "./docs/"  # 여기에 파일이 저장된 디렉토리 경로를 설정

db = SQLiteManager(DATABASE)

app.mount("/static", StaticFiles(directory="public"), name="static")

# 파일 추가 요청 모델
class FileRequest(BaseModel):
    filename: str
    
    
## /로 들어올때, public/index.html을 반환
@app.get("/")
async def root():
    file_path = os.path.join("public", "index.html")
    return FileResponse(file_path)

# 📌 1️⃣ 서버의 로컬 파일 목록을 반환하는 API
@app.get("/files")
async def list_files():
    try:
        files = os.listdir(FILE_DIRECTORY)
        return {"files": files}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Directory not found")

# # 📌 2️⃣ 선택한 파일을 DB에 저장하는 API
@app.get("/add_file")
async def add_file(filename: str):
    print(filename)
    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    file_path = os.path.join(FILE_DIRECTORY, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    tablename = str(generate_id())
    
    create_table(db, tablename)
    pdf_parser = pdfParse(file_path)
    save_parsed_data_to_db(pdf_parser, tablename, db, 0)
    save_parsed_data_to_db(pdf_parser, tablename, db, 1)
    
    return {"message": f"File '{filename}' added to database", "status": "success"}

# 📌 3️⃣ 파일을 검색하는 API
@app.get("/search")
async def search_files(q: str, tablename: str):
    division = ['개정', '신설']
    result = get_most_similar_paragraph(q, tablename, db)
    if not result:
        raise HTTPException(status_code=404, detail="No matching paragraph found")
    
    clause = [result[0]//1000, result[0]%1000]
    
    return {"results": f'{result[1]} {division[result[2]]}, {int(clause[0])}조 {int(clause[1])}항'}

@app.get("/tables")
async def list_tables():
    tables = get_tables(db)
    return {"tables": tables}

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
