import sqlite3

class SQLiteManager:
    def __init__(self, db_name):
        """Initialize the SQLiteManager with the database name."""
        self.db_name = db_name

    def connect(self):
        """Create a connection to the SQLite database."""
        return sqlite3.connect(self.db_name)

    def create_table(self, create_table_sql):
        """Create a table using the provided SQL statement."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
            print("Table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

    def insert(self, insert_sql, values):
        """Insert data into the table."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(insert_sql, values)
            conn.commit()
            print("Data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
        finally:
            conn.close()

    def select(self, select_sql, values=()):
        """Retrieve data from the table."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(select_sql, values)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Error retrieving data: {e}")
            return []
        finally:
            conn.close()

    def update(self, update_sql, values):
        """Update data in the table."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(update_sql, values)
            conn.commit()
            print("Data updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
        finally:
            conn.close()

    def delete(self, delete_sql, values):
        """Delete data from the table."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(delete_sql, values)
            conn.commit()
            print("Data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
        finally:
            conn.close()

# Example usage:
if __name__ == "__main__":
    db = SQLiteManager("example.db")
    
    
    
    # Creating a table
    # table 구성 
    
    # 1. id int(구분을 위한 컬럼)
    # 2. vector (문장, 문단의 벡터 변환값)
    # 3. division int(개정(0), 신설(1) 구분)
    # 4. date string(개정, 신설 날짜)
    # 5. clauses int(조항 번호, xxxyyy x:조 y:x조의 y에서 y)
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS legal_vectors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 고유 식별자
        vector BLOB NOT NULL,                  -- 문장 또는 문단의 벡터 변환 값
        division INTEGER NOT NULL,             -- 개정(0) 또는 신설(1)을 구분하는 값
        date TEXT NOT NULL,                    -- 개정 또는 신설 날짜 (문자열 형식)
        clauses INTEGER NOT NULL               -- 조항 번호 (xxxyyy 형식)
    );
    """
    db.create_table(create_table_query)
