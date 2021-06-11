import cv2
import imutils


def roi_parser(img):
    """
    Parses largest square roi (ie. the text)
    :param img:
    :return:
    """
    cnts = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return roi


if __name__ == "__main__":
    pass
