
# tests/test_task.py
import unittest
from datetime import datetime, timedelta
from models.task import Task, TaskStatus

class TestTask(unittest.TestCase):
    """Test cases for the Task model."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.due_date = datetime.now() + timedelta(days=1)
        self.task = Task(
            title="Test Task",
            description="Test Description",
            due_date=self.due_date
        )
        
    def test_task_initialization(self):
        """Test that a task is properly initialized with default values."""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "Test Description")
        self.assertEqual(self.task.status, TaskStatus.TODO)
        self.assertEqual(self.task.due_date, self.due_date)
        self.assertIsNone(self.task.id)
        
    def test_update_status(self):
        """Test that task status can be updated."""
        self.task.update_status(TaskStatus.IN_PROGRESS)
        self.assertEqual(self.task.status, TaskStatus.IN_PROGRESS)
        self.assertGreater(self.task.updated_at, self.task.created_at)
        
    def test_to_dict(self):
        """Test task conversion to dictionary."""
        task_dict = self.task.to_dict()
        self.assertEqual(task_dict["title"], "Test Task")
        self.assertEqual(task_dict["status"], "TODO")
        self.assertIn("created_at", task_dict)
        self.assertIn("updated_at", task_dict)
