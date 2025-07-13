
# --- services/task_service.py ---
import json
from typing import List
from models.task import Task
from utils.logger import logger
from unittest.mock import MagicMock  # Import for potential mocking


class TaskService:
    """Manages tasks, including creating, updating, deleting, and listing tasks."""

    def __init__(self, data_source: str = "tasks.json") -> None: # Mockable data source
        """Initializes the TaskService.

          Args:
              data_source: The source to read task data from, either 'tasks.json'
                or 'mock'. Default: 'tasks.json'.
        """
        self.data_source = data_source
        self.tasks: List[Task] = []
        if data_source == "tasks.json":
           self.load_tasks()
        # else, assume mock and don't load

    def load_tasks(self) -> None:
        """Loads tasks from the JSON file."""
        try:
            with open(self.data_source, "r") as f:
                tasks_data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in tasks_data]
                logger.info("Tasks loaded from file.")
        except FileNotFoundError:
            logger.warning(f"Data source file '{self.data_source}' not found.  Starting with empty task list.")
            self.tasks = []
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON in '{self.data_source}'. Starting with empty task list.")
            self.tasks = []
        except Exception as e:
            logger.exception(f"An unexpected error occurred while loading tasks: {e}")
            self.tasks = []


    def save_tasks(self) -> None:
        """Saves the current tasks to the JSON file."""
        try:
            with open(self.data_source, "w") as f:
                tasks_data = [task.to_dict() for task in self.tasks]
                json.dump(tasks_data, f, indent=4)  # Use indent for readability
            logger.info("Tasks saved to file.")
        except Exception as e:
            logger.exception(f"Error saving tasks to file: {e}")

    def create_task(self, title: str, description: str, due_date: str) -> Task:
        """Creates a new task.

        Args:
            title: The title of the task.
            description: The description of the task.
            due_date: The due date of the task.

        Returns:
            The newly created Task object.
        """
        try:
            if not all([title, description, due_date]):
                raise ValueError("All fields (title, description, due_date) are required.")
            next_id = max([task.task_id for task in self.tasks], default=0) + 1
            new_task = Task(next_id, title, description, due_date)
            self.tasks.append(new_task)
            self.save_tasks()
            logger.info(f"Task created: {new_task.title}")
            return new_task
        except ValueError as ve:
            logger.error(f"Error creating task: {ve}")
            raise
        except Exception as e:
            logger.exception(f"An unexpected error occurred while creating a task: {e}")
            raise


    def get_task(self, task_id: int) -> Task | None:
        """Retrieves a task by its ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The Task object if found, otherwise None.
        """
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        logger.warning(f"Task with ID {task_id} not found.")
        return None


    def update_task(self, task_id: int, title: str, description: str, due_date: str, status: str) -> Task | None:
        """Updates an existing task.

        Args:
            task_id: The ID of the task to update.
            title: The new title of the task.
            description: The new description of the task.
            due_date: The new due date of the task.
            status: The new status of the task.

        Returns:
            The updated Task object if successful, otherwise None.
        """
        task = self.get_task(task_id)
        if task:
            try:
                if not all([title, description, due_date, status]):
                    raise ValueError("All fields (title, description, due_date, status) are required for update.")

                task.title = title
                task.description = description
                task.due_date = due_date
                task.status = status
                self.save_tasks()
                logger.info(f"Task updated: {task.title}")
                return task
            except ValueError as ve:
                logger.error(f"Error updating task: {ve}")
                raise
            except Exception as e:
                logger.exception(f"Error updating task {task_id}: {e}")
                raise
        return None

    def delete_task(self, task_id: int) -> bool:
        """Deletes a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if the task was deleted successfully, False otherwise.
        """
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            logger.info(f"Task deleted: {task.title}")
            return True
        return False

    def list_all_tasks(self) -> List[Task]:
        """Lists all tasks.

        Returns:
            A list of all Task objects.
        """
        logger.info("Listing all tasks.")
        return self.tasks

