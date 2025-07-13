
# --- main.py ---
from services.task_service import TaskService
from models.task import Task
from utils.config import config
from utils.logger import logger
from typing import Optional, Dict, Any
import argparse



def command_line_interface() -> None:
    """Provides a command-line interface for the task management system."""

    parser = argparse.ArgumentParser(description="Task Management System")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create task command
    create_parser = subparsers.add_parser("create", help="Create a new task")
    create_parser.add_argument("title", type=str, help="Title of the task")
    create_parser.add_argument("description", type=str, help="Description of the task")
    create_parser.add_argument("due_date", type=str, help="Due date of the task (YYYY-MM-DD)")

    # List tasks command
    list_parser = subparsers.add_parser("list", help="List all tasks")

    # Get task command
    get_parser = subparsers.add_parser("get", help="Get a task by ID")
    get_parser.add_argument("task_id", type=int, help="ID of the task")

    # Update task command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("task_id", type=int, help="ID of the task to update")
    update_parser.add_argument("title", type=str, help="New title of the task")
    update_parser.add_argument("description", type=str, help="New description of the task")
    update_parser.add_argument("due_date", type=str, help="New due date of the task (YYYY-MM-DD)")
    update_parser.add_argument("status", type=str, help="New status of the task")

    # Delete task command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")

    args = parser.parse_args()

    task_service = TaskService(config.get("data_file", "tasks.json"))  # Use config

    if args.command == "create":
        try:
            task = task_service.create_task(args.title, args.description, args.due_date)
            print(f"Task created: {task}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "list":
        tasks = task_service.list_all_tasks()
        if tasks:
            for task in tasks:
                print(task)
        else:
            print("No tasks found.")

    elif args.command == "get":
        task = task_service.get_task(args.task_id)
        if task:
            print(task)
        else:
            print(f"Task with ID {args.task_id} not found.")

    elif args.command == "update":
        try:
            updated_task = task_service.update_task(args.task_id, args.title, args.description, args.due_date, args.status)
            if updated_task:
                print(f"Task updated: {updated_task}")
            else:
                print(f"Task with ID {args.task_id} not found.")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "delete":
        if task_service.delete_task(args.task_id):
            print(f"Task with ID {args.task_id} deleted.")
        else:
            print(f"Task with ID {args.task_id} not found.")
    else:
        parser.print_help()

