
# main.py
import argparse
import logging
from datetime import datetime
from pathlib import Path
from models.task import Task, TaskStatus
from services.task_service import TaskService
from utils.config import load_config
from utils.logger import get_logger

logger = get_logger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Task Management System")
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to configuration file"
    )
    return parser.parse_args()

def main():
    """Main entry point for the task management system."""
    args = parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Initialize services
    service = TaskService(config["database"]["path"])
    
    # Example usage
    task = Task(
        title="Complete project",
        description="Implement all required features",
        due_date=datetime.now()
    )
    
    # Create task
    created_task = service.create_task(task)
    logger.info(f"Created task: {created_task.to_dict()}")
    
    # Update task status
    updated_task = service.update_task_status(
        created_task.id,
        TaskStatus.IN_PROGRESS
    )
    logger.info(f"Updated task: {updated_task.to_dict()}")

if __name__ == "__main__":
    main()

# python main.py --config config.json

# coverage run -m unittest discover tests/
# coverage report