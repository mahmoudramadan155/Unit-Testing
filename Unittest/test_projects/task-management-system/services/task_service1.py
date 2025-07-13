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
        self._init_db()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with foreign key support enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
        
    def _init_db(self) -> None:
        """Initialize the database with required tables."""
        conn = self._get_connection()
        try:
            with conn:
                conn.executescript("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        status TEXT NOT NULL,
                        due_date TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    );
                """)
        finally:
            conn.close()
            
    def create_task(self, task: Task) -> Task:
        """Create a new task in the database."""
        conn = self._get_connection()
        try:
            with conn:
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
                logger.info(f"Created task with ID: {task.id}")
                return task
        finally:
            conn.close()
            
    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID."""
        conn = self._get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_task(row)
                return None
        finally:
            conn.close()
            
    def update_task_status(self, task_id: int, new_status: TaskStatus) -> Optional[Task]:
        """Update the status of a task."""
        task = self.get_task(task_id)
        if not task:
            return None
            
        task.update_status(new_status)
        
        conn = self._get_connection()
        try:
            with conn:
                conn.execute("""
                    UPDATE tasks
                    SET status = ?, updated_at = ?
                    WHERE id = ?
                """, (new_status.value, task.updated_at.isoformat(), task_id))
                
            logger.info(f"Updated task {task_id} status to {new_status.value}")
            return task
        finally:
            conn.close()