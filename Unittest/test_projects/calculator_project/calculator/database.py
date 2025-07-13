
# calculator/database.py
from typing import List

class DatabaseConnection:
    def query(self, sql: str) -> List[dict]:
        pass

    def close(self) -> None:
        pass

def create_test_database() -> DatabaseConnection:
    return DatabaseConnection()

def get_user_data(user_id: int) -> List[dict]:
    conn = DatabaseConnection()
    return conn.query(f"SELECT * FROM users WHERE id = {user_id}")
