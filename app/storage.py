"""Simple local persistence — saves profile + generated plan to a JSON file
in the user's home directory so data survives app restarts."""

import json
import os

APP_DIR = os.path.join(os.path.expanduser("~"), ".fitness_ai_planner")
DATA_FILE = os.path.join(APP_DIR, "data.json")


def save_data(profile: dict, targets: dict, workout_plan: dict, diet_plan: dict):
    os.makedirs(APP_DIR, exist_ok=True)
    payload = {
        "profile": profile,
        "targets": targets,
        "workout_plan": workout_plan,
        "diet_plan": diet_plan,
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
