## GradTimestamps

A small project to automatically get timestamps from UCSB's 2021 graduation ceremony stream.

Uses pytube/tqdm to download the videos, 
OpenCV to perform image processing, 
and Tesseract OCR/pytesseract (Untrained) to parse text from the image.

Outputs a text file of a list of timestamps, names, majors, and timestamped Youtube links.

The config.py file can be modified for some flexibility but I was a bit lazy so don't expect too much.
