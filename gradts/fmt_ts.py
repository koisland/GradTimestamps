import os
import json
import pprint

from config import Config
from helper import time_to


def format_timestamp(json_path):
    with open(json_path) as fobj:
        grads_dict = json.load(fobj)
        for grad_name, details in grads_dict.items():

            # pad nums in timestamp with zeroes
            timestamp = ':'.join(f"0{num}" if len(str(num)) == 1 else str(num) for num in details["Time"])
            secs = time_to(details["Time"], rtn_fmt="seconds")

            yield timestamp, grad_name, details["Major"], f"{Config.URL_TIMESTAMPED}{secs}s"


if __name__ == "__main__":
    json_file = os.path.join(Config.OUTPUT_DIR, "grads.json")
    grads = format_timestamp(json_file)
    with open(os.path.join(Config.OUTPUT_DIR, "grads.txt"), "w") as txt_file:
        for grad in grads:
            ts, name, major, link = grad
            txt_file.write(f"{ts} - {name} ({major}) - {link}\n")

