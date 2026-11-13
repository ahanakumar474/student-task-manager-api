import json
import os
import uuid

DATA_FILE = "tasks.json"


class Task:
    def __init__(self, title, subject, priority="Medium", due_date="", completed=False, task_id=None):
        self.id = task_id or str(uuid.uuid4())[:8]  # Short unique ID like 'a1b2c3d4'
        self.title = title.strip()
        self.subject = subject.strip() or "General"
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "subject": self.subject,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed
        }


def load_tasks():
    """Read tasks from the JSON file safely."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []


def save_tasks(tasks):
    """Save list of task dictionaries to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task(title, subject="General", priority="Medium", due_date=""):
    if not title or not title.strip():
        raise ValueError("Task title cannot be empty.")
    if priority not in ["Low", "Medium", "High"]:
        priority = "Medium"

    tasks = load_tasks()
    new_task = Task(title=title, subject=subject, priority=priority, due_date=due_date)
    tasks.append(new_task.to_dict())
    save_tasks(tasks)
    return new_task.to_dict()


def toggle_task_status(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            save_tasks(tasks)
            return task
    return None


def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [task for task in tasks if task["id"] != task_id]
    if len(updated_tasks) == len(tasks):
        return False
    save_tasks(updated_tasks)
    return True


# Quick test block (runs only when you run this file directly)
if __name__ == "__main__":
    t = add_task("Complete Python Mini Project", "CSDS Lab", "High", "2026-11-20")
    print("Added:", t)
    print("All Tasks:", load_tasks())