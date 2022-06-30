#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import cv2
import mimetypes


def is_a_video(input_file: Path) -> bool:
    mimetypes.init()
    mimestart = mimetypes.guess_type(input_file)[0]
    if mimestart is not None:
        mimestart = mimestart.split("/")[0]
        if mimestart == "video":
            return True
    return False


def extract_image_from_video(input_file: Path, output_directory: Path):
    if not is_a_video(input_file):
        raise Exception("The input file is not a video")

    cap = cv2.VideoCapture(input_file)
    count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            # cv2.imshow('window-name',frame)
            cv2.imwrite(output_directory / f"frame{count}.jpg", frame)
            count = count + 1
        else:
            break
        if cv2.waitKey(10) & 0xFF == ord("q"):  # press q to exit the program
            break

    print("Extraction is over")
    cap.release()
    cv2.destroyAllWindows()  # destroy all the opened windows
