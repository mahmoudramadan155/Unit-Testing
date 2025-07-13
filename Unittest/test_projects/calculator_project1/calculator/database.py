# calculator/database.py
from typing import List, Dict

class DatabaseConnection:
    def query(self, sql: str) -> List[Dict]:
        """Execute a SQL query."""
        pass

    def close(self) -> None:
        """Close the database connection."""
        pass

def create_test_database() -> DatabaseConnection:
    """Create a test database connection."""
    return DatabaseConnection()

def get_user_data(user_id: int) -> List[Dict]:
    """Get user data from database."""
    conn = DatabaseConnection()
    return conn.query(f"SELECT * FROM users WHERE id = {user_id}")