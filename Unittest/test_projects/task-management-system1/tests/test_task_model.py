
# --- tests/test_task_model.py ---
import unittest
from models.task import Task

class TestTaskModel(unittest.TestCase):
    """Test cases for the Task model."""

    def test_create_task(self) -> None:
        """Test creating a Task object."""
        task = Task(1, "Grocery Shopping", "Buy milk, eggs, and bread", "2024-03-15")
        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.title, "Grocery Shopping")
        self.assertEqual(task.description, "Buy milk, eggs, and bread")
        self.assertEqual(task.due_date, "2024-03-15")
        self.assertEqual(task.status, "To Do")  # Default status

    def test_task_to_dict(self) -> None:
        """Test converting a Task object to a dictionary."""
        task = Task(2, "Book Flight", "Book a flight to Hawaii", "2024-04-01", "In Progress")
        task_dict = task.to_dict()
        expected_dict = {
            "task_id": 2,
            "title": "Book Flight",
            "description": "Book a flight to Hawaii",
            "due_date": "2024-04-01",
            "status": "In Progress"
        }
        self.assertEqual(task_dict, expected_dict)

    def test_task_from_dict(self) -> None:
        """Test creating a Task object from a dictionary."""
        task_data = {
            "task_id": 3,
            "title": "Pay Bills",
            "description": "Pay electricity and water bills",
            "due_date": "2024-03-20",
            "status": "Completed"
        }
        task = Task.from_dict(task_data)
        self.assertEqual(task.task_id, 3)
        self.assertEqual(task.title, "Pay Bills")
        self.assertEqual(task.description, "Pay electricity and water bills")
        self.assertEqual(task.due_date, "2024-03-20")
        self.assertEqual(task.status, "Completed")

    def test_task_str(self) -> None:
        """Test the string representation of a Task object."""
        task = Task(4, "Meeting", "Team meeting at 10 AM", "2024-03-18")
        expected_str = "Task ID: 4, Title: Meeting, Description: Team meeting at 10 AM, Due Date: 2024-03-18, Status: To Do"
        self.assertEqual(str(task), expected_str)
