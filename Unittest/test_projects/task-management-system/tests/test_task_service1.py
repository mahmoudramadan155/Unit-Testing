
# tests/test_task_service.py
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from services.task_service import TaskService
from models.task import Task, TaskStatus

class TestTaskService(unittest.TestCase):
    """Test cases for the TaskService class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up any necessary test fixtures that can be shared across all tests."""
        pass
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Use in-memory database for testing
        self.service = TaskService(":memory:")
        
        # Create a sample task for testing
        self.test_task = Task(
            title="Test Task",
            description="Test Description",
            due_date=datetime.now()
        )
    
    def tearDown(self):
        """Clean up after each test method."""
        # The in-memory database is automatically cleared when all connections are closed
        pass
    
    def test_create_task(self):
        """Test creating a new task."""
        created_task = self.service.create_task(self.test_task)
        self.assertIsNotNone(created_task.id)
        
        # Verify task was stored
        retrieved_task = self.service.get_task(created_task.id)
        self.assertEqual(retrieved_task.title, self.test_task.title)
        
    def test_get_nonexistent_task(self):
        """Test retrieving a task that doesn't exist."""
        task = self.service.get_task(999)
        self.assertIsNone(task)
        
    def test_update_task_status(self):
        """Test updating a task's status."""
        # First create a task
        task = self.service.create_task(self.test_task)
        
        # Update its status
        updated_task = self.service.update_task_status(
            task.id,
            TaskStatus.IN_PROGRESS
        )
        
        self.assertEqual(updated_task.status, TaskStatus.IN_PROGRESS)
        self.assertGreater(updated_task.updated_at, updated_task.created_at)
        
    def test_update_nonexistent_task(self):
        """Test updating a task that doesn't exist."""
        updated_task = self.service.update_task_status(
            999,
            TaskStatus.IN_PROGRESS
        )
        self.assertIsNone(updated_task)
        