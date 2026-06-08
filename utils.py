import json
import os


def load_json(filename):
    if not os.path.exists(filename):
        return {}

    try:
        with open(
            filename,
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    except Exception as e:
        print(f"JSON Error: {e}")
    return {}


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
