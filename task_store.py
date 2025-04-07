
import json
from pathlib import Path

STORE_FILE = "seen_tasks.json"

def load_seen_tasks():
    if not Path(STORE_FILE).exists():
        return []
    
    with open(STORE_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:  # Handle empty file
            return []
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return []  # Return empty list if JSON is invalid

def save_seen_tasks(tasks):
    # Only save if we have tasks to save
    if tasks:
        with open(STORE_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)

def get_new_tasks(current_tasks, seen_tasks):
    # Create set of seen task IDs
    seen_ids = {t["id"] for t in seen_tasks}
    
    # Return tasks that haven't been seen before
    return [task for task in current_tasks if task["id"] not in seen_ids]
