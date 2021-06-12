import os
import json

from config import Config


def timestamp_to_text(json_path):
    grad_days = json.load(open(json_path))
    for day, grads in grad_days:
        with open(os.path.join(Config.OUTPUT_DIR, f"grads_{day}.txt"), "w") as txt_file:
            for name, info in grads:
                txt_file.write(f"{info['Timestamp']} - {name} ({info['Major']}) - {info['Link']}\n")


if __name__ == "__main__":
    json_file = os.path.join(Config.OUTPUT_DIR, "grads.json")
    timestamp_to_text(json_file)
