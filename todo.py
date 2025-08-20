import json
import os
from typing import Optional
from flask import Flask, render_template, request, redirect, url_for


class TodoApp:
    """Simple Todo application with file persistence."""

    def __init__(self, storage_path: Optional[str] = None) -> None:
        self.storage_path = storage_path or os.environ.get("TASKS_PATH", "tasks.json")
        self.tasks: list[str] = []
        self.load()

    def load(self) -> None:
        """Load tasks from the storage file if it exists."""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if isinstance(data, list):
                        self.tasks = [str(item) for item in data]
                    else:
                        self.tasks = []
            else:
                self.tasks = []
        except Exception:
            # If file is missing or corrupt, start with an empty list
            self.tasks = []

    def save(self) -> None:
        """Persist tasks to the storage file."""
        try:
            with open(self.storage_path, "w", encoding="utf-8") as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=2)
        except Exception as error:
            print(f"Failed to save tasks: {error}")

    def add_task(self, task: str) -> None:
        task = task.strip()
        if not task:
            print("Cannot add an empty task.")
            return
        self.tasks.append(task)
        self.save()
        print(f"Added: {task}")

    def list_tasks(self) -> None:
        if not self.tasks:
            print("No tasks yet!")
        else:
            for i, task in enumerate(self.tasks, 1):
                print(f"{i}. {task}")

    def delete_task(self, task_number: int) -> None:
        """Delete a task by its 1-based number."""
        if 1 <= task_number <= len(self.tasks):
            removed = self.tasks.pop(task_number - 1)
            self.save()
            print(f"Deleted: {removed}")
        else:
            print("Invalid task number.")


# Flask web application
flask_app = Flask(__name__)
todo_app = TodoApp()


@flask_app.route("/", methods=["GET"])
def index():
    return render_template("index.html", tasks=todo_app.tasks)


@flask_app.route("/add", methods=["POST"])
def add():
    task_text = request.form.get("task", "")
    todo_app.add_task(task_text)
    return redirect(url_for("index"))


@flask_app.route("/delete/<int:number>", methods=["POST"])
def delete(number: int):
    todo_app.delete_task(number)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Start the Flask development server
    flask_app.run(debug=True)
