
# services/task_service.py
import sqlite3
from typing import List, Optional
from datetime import datetime
import logging
from models.task import Task, TaskStatus
from utils.logger import get_logger

logger = get_logger(__name__)

class TaskService:
    """Service class for managing tasks in the database."""
    
    def __init__(self, db_path: str):
        """
        Initialize the TaskService with a database connection.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        # Initialize database immediately upon creation
        self._init_db()
        
    def _init_db(self) -> None:
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            # Ensure the changes are committed
            conn.commit()
            
    def create_task(self, task: Task) -> Task:
        """
        Create a new task in the database.
        
        Args:
            task (Task): Task object to be created
            
        Returns:
            Task: Created task with assigned ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (title, description, status, due_date, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                task.title,
                task.description,
                task.status.value,
                task.due_date.isoformat(),
                task.created_at.isoformat(),
                task.updated_at.isoformat()
            ))
            task.id = cursor.lastrowid
            # Ensure the transaction is committed
            conn.commit()
            logger.info(f"Created task with ID: {task.id}")
            return task
            
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        
        Args:
            task_id (int): ID of the task to retrieve
            
        Returns:
            Optional[Task]: Task object if found, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_task(row)
            return None
            
    def update_task_status(self, task_id: int, new_status: TaskStatus) -> Optional[Task]:
        """
        Update the status of a task.
        
        Args:
            task_id (int): ID of the task to update
            new_status (TaskStatus): New status to set
            
        Returns:
            Optional[Task]: Updated task if found, None otherwise
        """
        task = self.get_task(task_id)
        if not task:
            return None
            
        task.update_status(new_status)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE tasks
                SET status = ?, updated_at = ?
                WHERE id = ?
            """, (new_status.value, task.updated_at.isoformat(), task_id))
            
        logger.info(f"Updated task {task_id} status to {new_status.value}")
        return task
            
    def _row_to_task(self, row: tuple) -> Task:
        """Convert a database row to a Task object."""
        task = Task(
            title=row[1],
            description=row[2],
            due_date=datetime.fromisoformat(row[4]),
            task_id=row[0]
        )
        task.status = TaskStatus(row[3])
        task.created_at = datetime.fromisoformat(row[5])
        task.updated_at = datetime.fromisoformat(row[6])
        return task
