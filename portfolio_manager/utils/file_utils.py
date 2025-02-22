import json
from pathlib import Path

def read_json(file_path):
    """Read data from a JSON file."""
    if Path(file_path).exists():
        with open(file_path, "r") as file:
            return json.load(file)
    return {}

def write_json(file_path, data):
    """Write data to a JSON file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)