# tests/test_task_service.py (Corrected)
import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os
from services.task_service import TaskService
from models.task import Task


class TestTaskService(unittest.TestCase):
    """Test cases for the TaskService."""

    def setUp(self):
        """Setup method to create a TaskService instance before each test."""
        self.task_service = TaskService(data_source="mock")
        self.test_task_data = [
            {"task_id": 1, "title": "Test Task 1", "description": "Description 1", "due_date": "2024-03-15", "status": "To Do"},
            {"task_id": 2, "title": "Test Task 2", "description": "Description 2", "due_date": "2024-03-20", "status": "In Progress"}
        ]

    def tearDown(self):
        """Teardown method."""
        pass # No resources to clean up in this example, but good practice to include



    @patch('services.task_service.TaskService.load_tasks')  # Mock load_tasks for create_task
    @patch('services.task_service.TaskService.save_tasks') # Mock save_tasks for create_task
    def test_create_task(self, mocked_save_tasks: MagicMock, mocked_load_tasks: MagicMock) -> None:
        """Test creating a task."""

        mocked_load_tasks.return_value = None  # Simulate successful loading
        mocked_save_tasks.return_value = None

        new_task = self.task_service.create_task("New Task", "New Description", "2024-03-25")
        self.assertIsInstance(new_task, Task)
        self.assertEqual(new_task.title, "New Task")
        self.assertEqual(len(self.task_service.tasks), 1) # Ensure task list is updated
        mocked_save_tasks.assert_called_once()


    @patch('services.task_service.TaskService.save_tasks')
    def test_create_task_missing_fields(self, mocked_save_tasks : MagicMock):
        """Test creating a task with missing fields, should raise ValueError."""
        with self.assertRaises(ValueError):
            self.task_service.create_task("", "Description", "2024-03-25")  # Missing title
        mocked_save_tasks.assert_not_called()


    def test_get_task(self):
        """Test retrieving a task by ID."""
        self.task_service.tasks = [Task.from_dict(task_data) for task_data in self.test_task_data]
        task = self.task_service.get_task(1)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, "Test Task 1")
        not_found_task = self.task_service.get_task(99)  # Non-existent ID
        self.assertIsNone(not_found_task)


    @patch('services.task_service.TaskService.save_tasks')
    def test_update_task(self, mocked_save_tasks: MagicMock):
        """Test updating a task."""
        self.task_service.tasks = [Task.from_dict(task_data) for task_data in self.test_task_data]
        updated_task = self.task_service.update_task(1, "Updated Title", "Updated Description", "2024-03-22", "Completed")
        mocked_save_tasks.assert_called_once()
        self.assertIsInstance(updated_task, Task)
        self.assertEqual(updated_task.title, "Updated Title")
        # Check that task in task_service's list is updated:
        self.assertEqual(self.task_service.tasks[0].title, "Updated Title")
        not_found_task = self.task_service.update_task(99, "Title", "Desc", "2024-04-01", "To Do") # Non-existent ID
        self.assertIsNone(not_found_task)


    @patch('services.task_service.TaskService.save_tasks')
    def test_update_task_missing_field(self, mocked_save_tasks: MagicMock) -> None:
            """Ensure ValueError if fields are missing."""
            self.task_service.tasks = [Task.from_dict(data) for data in self.test_task_data]
            with self.assertRaises(ValueError):
                self.task_service.update_task(1, "", "Updated Desc", "2024-04-04", "Done")
            mocked_save_tasks.assert_not_called()


    @patch('services.task_service.TaskService.save_tasks')
    def test_delete_task(self, mocked_save_tasks: MagicMock):
        """Test deleting a task."""
        self.task_service.tasks = [Task.from_dict(task_data) for task_data in self.test_task_data]
        result = self.task_service.delete_task(1)
        mocked_save_tasks.assert_called_once()
        self.assertTrue(result)
        self.assertEqual(len(self.task_service.tasks), 1)  # Check task is removed
        not_found_result = self.task_service.delete_task(99)  # Non-existent ID
        self.assertFalse(not_found_result)


    def test_list_all_tasks(self) -> None:
        """Test listing all tasks."""
        self.task_service.tasks = [Task.from_dict(task_data) for task_data in self.test_task_data]
        tasks = self.task_service.list_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertIsInstance(tasks[0], Task)

    @patch("builtins.open", new_callable=mock_open, read_data='[{"task_id": 1, "title": "Task 1", "description": "Desc 1", "due_date": "2024-12-12", "status": "Done"}]')
    def test_load_tasks_success(self, mock_file):
        ts = TaskService(data_source='dummy.json')
        ts.load_tasks()  # Explicitly call load_tasks
        mock_file.assert_called_with('dummy.json', 'r')
        self.assertEqual(len(ts.tasks), 1)
        self.assertEqual(ts.tasks[0].title, 'Task 1')


    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_tasks_file_not_found(self, mock_open_func):
        ts = TaskService(data_source='no_file.json')
        ts.load_tasks()  # Explicitly call load_tasks
        mock_open_func.assert_called_once_with("no_file.json", 'r')
        self.assertEqual(len(ts.tasks), 0) # Should be empty list

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_load_tasks_json_decode_error(self, mock_file):
        ts = TaskService(data_source='invalid.json')
        ts.load_tasks() # Explicitly call load_tasks
        mock_file.assert_called_with('invalid.json', "r")
        self.assertEqual(len(ts.tasks), 0) # Should be an empty list


    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_tasks(self, mock_json_dump, mock_file_open):
        ts = TaskService(data_source='test_tasks.json')
        ts.tasks = [Task.from_dict(data) for data in self.test_task_data]
        ts.save_tasks()

        mock_file_open.assert_called_once_with('test_tasks.json', 'w')
        mock_json_dump.assert_called_once()

        # More precise check of what was written:
        args, kwargs = mock_json_dump.call_args
        written_data = args[0]  # first positional argument
        self.assertEqual(len(written_data), 2)
        self.assertEqual(written_data[0]['title'], "Test Task 1")
