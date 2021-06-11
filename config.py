import datetime
import os


class Config:
    # main file stuff
    URLS = ("https://www.youtube.com/watch?v=p5thqkhj38A", "https://www.youtube.com/watch?v=B3i-h43kErU",
            "https://www.youtube.com/watch?v=48x3MLWXjS4", "https://www.youtube.com/watch?v=gA1XNaEuvME")
    START_TIME = (0, 18, 40)
    URLS_TIMESTAMPED = [f"{url}&t=" for url in URLS]
    SRCS_DIR = os.path.join(os.path.dirname(__file__), "srcs")
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
    BBOX = {"X": (100, 590), "Y": (265, 335)}

    DEFAULT_DATE = datetime.datetime.now()
    DEFAULT_FPS = 30

    # pytube stuff
    VALID_RESOLUTIONS = ("144p", "240p", "360p", "480p", "720p", "1080p")
