import os


class Config:
    # main file stuff
    URL = "https://www.youtube.com/watch?v=p5thqkhj38A"
    URL_TIMESTAMPED = "https://youtu.be/p5thqkhj38A?t="
    SRCS_DIR = os.path.join(os.path.dirname(__file__), "srcs")
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
    BBOXES = {"X": (100, 590), "Y": (265, 335)}

    # pytube stuff
    VALID_RESOLUTIONS = ("144p", "240p", "360p", "480p", "720p", "1080p")
