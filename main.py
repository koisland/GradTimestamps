import os
import json

import cv2
import imutils
import pytesseract

from gradts.downloader import PytubeDl
from gradts.helper import time_to
from config import Config


if __name__ == "__main__":
    try:
        # download video with pytube
        dl = PytubeDl(url=Config.URLS[0], output_dir=Config.SRCS_DIR, media_type="video_only", res="720p")
        grad_video = dl.download()

        # set date and fps
        date = dl.pytube_obj.publish_date
        fps = dl.fps
    except Exception:
        # set defaults if fails to download.
        grad_video = os.path.join(Config.SRCS_DIR, "Grad Walk  June 7 2021.mp4")
        date = Config.DEFAULT_DATE
        fps = Config.DEFAULT_FPS

    # format date
    date = f"{date.month}_{date.day}_{date.year}"

    # set grad data output dir
    data = os.path.join(Config.OUTPUT_DIR, f"grads_{date}.json")
    people = {}

    video = cv2.VideoCapture(grad_video)

    # 7 hrs, 28 mins, 45 secs -> 26925 secs
    video_length_frames = time_to((7, 28, 45), rtn_fmt="frames", fps=fps)
    start_time_frames = time_to((0, 18, 40), rtn_fmt="frames", fps=fps)

    # CAP_PROP_FRAME_COUNT sets frame position of capture.
    video.set(cv2.CAP_PROP_POS_FRAMES, start_time_frames)

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        # resize, grayscale,  blur, threshold and invert image.
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
        inv = cv2.bitwise_not(thresh)

        # TODO: Find way to automate. use cv2.inrange with blue bgr?
        # set bbox of roi. format is {"X": (x0, x1), "Y": (y0, y1)}
        bbox = Config.BBOXES
        crop = inv[bbox["Y"][0]:bbox["Y"][1], bbox["X"][0]:bbox["X"][1]]

        # FOR DEBUGGING
        cv2.imshow(f"gray_{start_time_frames}", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Convert image roi to string
        text = pytesseract.image_to_string(crop)

        # remove empty text and get first two pieces of text sep by newline char.
        split_text = [txt for txt in text.split("\n")[0:3] if txt]

        # split into name and major.
        if len(split_text) >= 2:
            name, major = split_text[0:2]

            # convert video frame number into time into hours, minute, and seconds
            time = time_to(start_time_frames, fps)

            # add to dict if hasn't be added taking first time found.
            if people.get(name) is None:
                people[name] = {"Time": time, "Major": major}

        # skip every 120th frame ie. 4 secs
        start_time_frames += 120
        video.set(cv2.CAP_PROP_POS_FRAMES, start_time_frames)

    # dump dict into json
    json = json.dumps(people)
    file = open(data, "w")
    file.write(json)
    file.close()

    # close vid capture
    video.release()
