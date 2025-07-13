# --- models/task.py ---
class Task:
    """Represents a task in the task management system."""

    def __init__(self, task_id: int, title: str, description: str, due_date: str, status: str = "To Do") -> None:
        """Initializes a Task object.

        Args:
            task_id (int): Unique identifier for the task.
            title (str): Title of the task.
            description (str): Description of the task.
            due_date (str): Due date of the task (e.g., "YYYY-MM-DD").
            status (str, optional): Current status of the task. Defaults to "To Do".
        """
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status

    def __str__(self) -> str:
        """Returns a string representation of the task."""
        return (f"Task ID: {self.task_id}, Title: {self.title}, "
                f"Description: {self.description}, Due Date: {self.due_date}, Status: {self.status}")

    def to_dict(self) -> dict:
        """Converts the task to a dictionary."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Creates a Task object from a dictionary."""
        return cls(data['task_id'], data['title'], data['description'], data['due_date'], data['status'])
