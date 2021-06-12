import os
import json

from config import Config


def timestamp_to(json_path, file_type="md"):
    try:
        grad_dict = json.load(open(json_path))
    except Exception:
        raise Exception(f"Can't open file. {json_path}")

    file_n_ext = os.path.split(json_path)[1]
    file_name = os.path.splitext(file_n_ext)[0]

    # format message line
    messages = {
        "txt": lambda name, timestamp, link, major: f"{timestamp} - {name} ({major}) - {link}\n",
        "md": lambda name, timestamp, link, major: f"- [{timestamp}]({link}) - {name} ({major})\n"
    }

    with open(os.path.join(Config.OUTPUT_DIR, f"{file_name}.{file_type}"), "w") as file_obj:
        for grad, info in grad_dict.items():
            msg_args = (grad, *info.values())
            if msg := messages.get(file_type):
                file_obj.write(msg(*msg_args))
            else:
                raise Exception("Invalid file type.")


if __name__ == "__main__":
    for file in os.listdir(Config.OUTPUT_DIR):
        if ".json" in file:
            file_path = os.path.join(Config.OUTPUT_DIR, file)
            timestamp_to(file_path, file_type="md")

