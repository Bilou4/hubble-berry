#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import os
import mimetypes


def is_a_video(input_file: str) -> bool:
    mimetypes.init()
    mimestart = mimetypes.guess_type(input_file)[0]
    if mimestart != None:
        mimestart = mimestart.split("/")[0]
        if mimestart == "video":
            return True
    return False


def extract_image_from_video(input_file, output_directory):
    if is_a_video(input_file) and os.path.isdir(output_directory):
        if output_directory[-1] != "/":
            output_directory = output_directory + "/"
    else:
        raise Exception(
            "Either the input is not a video file or the output is not a directory"
        )

    cap = cv2.VideoCapture(input_file)
    count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            # cv2.imshow('window-name',frame)
            cv2.imwrite(output_directory + "frame%d.jpg" % count, frame)
            count = count + 1
        else:
            break
        if cv2.waitKey(10) & 0xFF == ord("q"):  # press q to exit the program
            break

    print("[\033[0;32m OK\033[0m ] Extraction is over")
    cap.release()
    cv2.destroyAllWindows()  # destroy all the opened windows
