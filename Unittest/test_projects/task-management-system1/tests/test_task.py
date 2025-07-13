# tests/test_task.py
import unittest
from models.task import Task

class TestTask(unittest.TestCase):

    def setUp(self):
        """Setup method to create Task instances before each test."""
        self.task1 = Task(1, "Grocery Shopping", "Buy milk, eggs, bread", "2024-03-15")
        self.task2 = Task(2, "Book Flight", "Book flight to London", "2024-04-01", "In Progress")
        self.task3_data = {
            "task_id": 3,
            "title": "Pay Bills",
            "description": "Electricity and water bills",
            "due_date": "2024-03-20",
            "status": "Completed"
        }
        self.task3 = Task.from_dict(self.task3_data)


    def test_create_task(self):
        """Test Task object creation."""
        self.assertEqual(self.task1.task_id, 1)
        self.assertEqual(self.task1.title, "Grocery Shopping")
        self.assertEqual(self.task1.description, "Buy milk, eggs, bread")
        self.assertEqual(self.task1.due_date, "2024-03-15")
        self.assertEqual(self.task1.status, "To Do") #default

        self.assertEqual(self.task2.task_id, 2)
        self.assertEqual(self.task2.title, "Book Flight")
        self.assertEqual(self.task2.description, "Book flight to London")
        self.assertEqual(self.task2.due_date, "2024-04-01")
        self.assertEqual(self.task2.status, "In Progress")


    def test_task_to_dict(self):
        """Test converting Task object to dictionary."""
        expected_dict1 = {
            "task_id": 1,
            "title": "Grocery Shopping",
            "description": "Buy milk, eggs, bread",
            "due_date": "2024-03-15",
            "status": "To Do"
        }
        self.assertEqual(self.task1.to_dict(), expected_dict1)

        expected_dict2 = {
            "task_id": 2,
            "title": "Book Flight",
            "description": "Book flight to London",
            "due_date": "2024-04-01",
            "status": "In Progress"
        }
        self.assertEqual(self.task2.to_dict(), expected_dict2)

    def test_task_from_dict(self):
        """Test creating Task object from a dictionary"""
        task = Task.from_dict(self.task3_data)
        self.assertEqual(task.task_id, 3)
        self.assertEqual(task.title, "Pay Bills")
        self.assertEqual(task.description, "Electricity and water bills")
        self.assertEqual(task.due_date, "2024-03-20")
        self.assertEqual(task.status, "Completed")
        self.assertIsInstance(task, Task)  # Good practice to check the type

    def test_task_str(self):
        """Test __str__ method"""
        expected_str = "Task ID: 1, Title: Grocery Shopping, Description: Buy milk, eggs, bread, Due Date: 2024-03-15, Status: To Do"
        self.assertEqual(str(self.task1), expected_str)
        expected_str2 = "Task ID: 2, Title: Book Flight, Description: Book flight to London, Due Date: 2024-04-01, Status: In Progress"
        self.assertEqual(str(self.task2), expected_str2)