import os
import json
from collections import defaultdict

import cv2
import imutils
import pytesseract

from gradts.logger import get_logger
from gradts.downloader import PytubeDl, dl_multiple
from gradts.helper import time_to
from config import Config

log = get_logger()

if __name__ == "__main__":

    log.info("Starting.")

    for v_info in dl_multiple(video_list=Config.URLS, output=Config.SRCS_DIR):

        date, fps, grad_video = v_info

        # set grad data output dir
        data = os.path.join(Config.OUTPUT_DIR, f"grads_{date}.json")
        grads = {}

        video = cv2.VideoCapture(grad_video)

        start_time_frames = time_to(Config.START_TIME, rtn_fmt="frames", fps=fps)

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
                if grads.get(name) is None:
                    log.info(f"{name} @ {time}")
                    grads[name] = {"Time": time, "Major": major}

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
        log.info("Finished.")
