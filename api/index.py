import os
from todo import flask_app as app

# Ensure a writable path for serverless runtime
os.environ.setdefault("TASKS_PATH", "/tmp/tasks.json")
