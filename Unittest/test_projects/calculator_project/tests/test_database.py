# tests/test_database.py
import unittest
from unittest.mock import Mock, patch
from calculator.database import DatabaseConnection, get_user_data

class TestDatabase(unittest.TestCase):
    def test_database_query(self):
        mock_db = Mock()
        mock_db.query.return_value = [
            {"id": 123, "name": "Test User", "email": "test@example.com"}
        ]
        
        with patch('calculator.database.DatabaseConnection', return_value=mock_db):
            results = get_user_data(user_id=123)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["name"], "Test User")
            mock_db.query.assert_called_once()

if __name__ == '__main__':
    unittest.main()