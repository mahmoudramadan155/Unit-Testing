
# models/task.py
from datetime import datetime
from typing import Optional, Dict
from enum import Enum
import time

class TaskStatus(Enum):
    """Enumeration for possible task statuses."""
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class Task:
    """
    Represents a task in the task management system.
    
    Attributes:
        id (int): Unique identifier for the task
        title (str): Title of the task
        description (str): Detailed description of the task
        status (TaskStatus): Current status of the task
        due_date (datetime): Due date for the task completion
        created_at (datetime): Task creation timestamp
        updated_at (datetime): Last update timestamp
    """
    
    def __init__(
        self,
        title: str,
        description: str,
        due_date: datetime,
        task_id: Optional[int] = None
    ) -> None:
        self.id = task_id
        self.title = title
        self.description = description
        self.status = TaskStatus.TODO
        self.due_date = due_date
        self.created_at = datetime.now()
        # Ensure updated_at is initially the same as created_at
        self.updated_at = self.created_at
        
    def update_status(self, new_status: TaskStatus) -> None:
        """Updates the task status and the updated_at timestamp."""
        self.status = new_status
        # Add a small delay to ensure updated_at is different from created_at
        time.sleep(0.001)
        self.updated_at = datetime.now()
        
    def to_dict(self) -> Dict:
        """Converts the task object to a dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "due_date": self.due_date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
