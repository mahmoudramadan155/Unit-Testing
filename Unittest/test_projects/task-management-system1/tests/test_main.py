# --- tests/test_main.py ---
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import os
from main import command_line_interface
from services.task_service import TaskService


class TestCommandLineInterface(unittest.TestCase):
    def setUp(self):
        """Setup before each test.  Creates a TaskService and redirects stdout."""
        self.task_service_patch = patch('main.TaskService', autospec=True)  #Patch TaskService creation
        self.mock_task_service = self.task_service_patch.start()
        self.mock_task_service_instance = MagicMock(spec=TaskService) # instance to return
        self.mock_task_service.return_value = self.mock_task_service_instance
        self.captured_output = StringIO()  # Redirect stdout for testing output
        sys.stdout = self.captured_output

    def tearDown(self):
        """Clean up after each test."""
        sys.stdout = sys.__stdout__  # Restore stdout
        self.task_service_patch.stop()

    @patch('sys.argv', ['main.py', 'create', 'My Task', 'Do something', '2024-12-31'])
    def test_create_command(self):
        """Test the 'create' command."""
        # Mock the return from create_task
        mock_task = MagicMock()
        mock_task.__str__.return_value = "Mocked Task"  # For printing
        self.mock_task_service_instance.create_task.return_value = mock_task

        command_line_interface()

        # Check create_task was called with correct arguments
        self.mock_task_service_instance.create_task.assert_called_once_with(
            "My Task", "Do something", "2024-12-31"
        )
        # Check that the correct output gets printed:
        self.assertEqual(self.captured_output.getvalue().strip(), "Task created: Mocked Task")

    @patch('sys.argv', ['main.py', 'create', '', 'Do something', '2024-12-31'])
    def test_create_command_error(self):
        self.mock_task_service_instance.create_task.side_effect = ValueError("Title required")
        command_line_interface()
        self.assertIn("Error: Title required", self.captured_output.getvalue())


    @patch('sys.argv', ['main.py', 'list'])
    def test_list_command(self):
        """Test the 'list' command."""
        # Setup two mock tasks
        mock_task1 = MagicMock()
        mock_task1.__str__.return_value = "Task 1"
        mock_task2 = MagicMock()
        mock_task2.__str__.return_value = "Task 2"

        # set the return value for list_all_tasks
        self.mock_task_service_instance.list_all_tasks.return_value = [mock_task1, mock_task2]

        command_line_interface()

        # Check calls and output
        self.mock_task_service_instance.list_all_tasks.assert_called_once()
        output_lines = self.captured_output.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 2)
        self.assertEqual(output_lines[0], "Task 1")
        self.assertEqual(output_lines[1], "Task 2")


    @patch('sys.argv', ['main.py', 'list'])
    def test_list_command_no_tasks(self):
        self.mock_task_service_instance.list_all_tasks.return_value = []
        command_line_interface()
        self.assertEqual(self.captured_output.getvalue().strip(), "No tasks found.")

    @patch('sys.argv', ['main.py', 'get', '1'])
    def test_get_command(self):
        mock_task = MagicMock()
        mock_task.__str__.return_value = "Retrieved Task"
        self.mock_task_service_instance.get_task.return_value = mock_task
        command_line_interface()
        self.mock_task_service_instance.get_task.assert_called_once_with(1)
        self.assertEqual(self.captured_output.getvalue().strip(), "Retrieved Task")


    @patch('sys.argv', ['main.py', 'get', '99'])
    def test_get_command_not_found(self):
        self.mock_task_service_instance.get_task.return_value = None
        command_line_interface()
        self.mock_task_service_instance.get_task.assert_called_once_with(99)
        self.assertEqual(self.captured_output.getvalue().strip(), "Task with ID 99 not found.")



    @patch('sys.argv', ['main.py', 'update', '1', 'New Title', 'New Desc', '2024-05-05', 'Done'])
    def test_update_command(self):
        """Test the update command."""
        mock_task = MagicMock()
        mock_task.__str__.return_value = "Updated Task"
        self.mock_task_service_instance.update_task.return_value = mock_task
        command_line_interface()

        self.mock_task_service_instance.update_task.assert_called_once_with(
            1, "New Title", "New Desc", "2024-05-05", "Done"
        )
        self.assertEqual(self.captured_output.getvalue().strip(), "Task updated: Updated Task")

    @patch('sys.argv', ['main.py', 'update', '1', '', 'New Desc', '2024-05-05', 'Done'])
    def test_update_command_error(self):
        self.mock_task_service_instance.update_task.side_effect = ValueError("Title cannot be empty")
        command_line_interface()
        self.assertIn("Error: Title cannot be empty", self.captured_output.getvalue())


    @patch('sys.argv', ['main.py', 'update', '99', 'New Title', 'New Desc', '2024-05-05', 'Done'])
    def test_update_command_not_found(self):
        self.mock_task_service_instance.update_task.return_value = None
        command_line_interface()
        self.assertEqual(self.captured_output.getvalue().strip(), "Task with ID 99 not found.")

    @patch('sys.argv', ['main.py', 'delete', '1'])
    def test_delete_command(self):
        """Test the delete command."""
        self.mock_task_service_instance.delete_task.return_value = True
        command_line_interface()
        self.mock_task_service_instance.delete_task.assert_called_once_with(1)
        self.assertEqual(self.captured_output.getvalue().strip(), "Task with ID 1 deleted.")

    @patch('sys.argv', ['main.py', 'delete', '99'])
    def test_delete_command_not_found(self):
        """Test delete command when task not found."""
        self.mock_task_service_instance.delete_task.return_value = False # Simulate not found
        command_line_interface()
        self.mock_task_service_instance.delete_task.assert_called_once_with(99)
        self.assertEqual(self.captured_output.getvalue().strip(), "Task with ID 99 not found.")


    @patch('sys.argv', ['main.py']) # No arguments provided
    @patch('argparse.ArgumentParser.print_help')
    def test_no_command(self, mock_print_help):
        """Test behavior when no command is provided."""
        command_line_interface()
        mock_print_help.assert_called_once()

