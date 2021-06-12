import os
import json

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

    for v_info, link in zip(dl_multiple(video_list=Config.URLS, output=Config.SRCS_DIR), Config.URLS_TIMESTAMPED):

        date, fps, grad_video = v_info

        # set grad data output dir
        grad_list = os.path.join(Config.OUTPUT_DIR, f"grads_{date}.json")
        grads = {}

        video = cv2.VideoCapture(grad_video)

        start_time_frames = time_to(Config.START_TIME, rtn_fmt="frames", fps=fps)

        # CAP_PROP_FRAME_COUNT sets frame position of capture.
        video.set(cv2.CAP_PROP_POS_FRAMES, start_time_frames)

        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            # resize, grayscale, threshold and invert image.
            frame = imutils.resize(frame, width=600)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            inv = cv2.bitwise_not(thresh)

            # TODO: Find way to automate. use cv2.inrange with blue bgr?
            # set bbox of roi. format is {"X": (x0, x1), "Y": (y0, y1)}
            bbox = Config.BBOX
            crop = inv[bbox["Y"][0]:bbox["Y"][1], bbox["X"][0]:bbox["X"][1]]

            # FOR DEBUGGING
            # cv2.imshow(f"frame_{start_time_frames}", crop)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # Convert image roi to string
            text = pytesseract.image_to_string(crop, config=f"-c tessedit_char_whitelist={Config.CHAR_WHITELIST}")

            # remove empty text and get first two pieces of text sep by newline char.
            split_text = [txt for txt in text.split("\n")[0:3] if txt]

            # split into name and major.
            if len(split_text) >= 2:
                name, major = split_text[0:2]

                # convert video frame number into time into hours, minute, and seconds
                time = time_to(start_time_frames, fps)

                # add to dict if hasn't be added taking first time found.
                if grads.get(name) is None:
                    # pad nums in timestamp with zeroes
                    timestamp = ':'.join(f"0{num}" if len(str(num)) == 1 else str(num) for num in time)
                    secs = time_to(time, rtn_fmt="seconds")
                    link = f"{link}{secs}s"

                    log.info(f"{name} @ {time} on {date}")
                    grads[name] = {"Timestamp": timestamp, "Link": link, "Major": major}

            # skip desired number of seconds
            start_time_frames += (Config.SKIP_EVERY * fps)
            video.set(cv2.CAP_PROP_POS_FRAMES, start_time_frames)

        # dump dict into json
        json = json.dumps(grads)
        file = open(grad_list, "w")
        file.write(json)
        file.close()

        # close vid capture
        video.release()
        log.info("Finished.")
