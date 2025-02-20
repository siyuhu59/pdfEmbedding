def get_tables(db):
    
    """DB에 존재하는 모든 테이블 목록을 반환"""
    db.connect()
    rows = db.select("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in rows]
    
    return tables