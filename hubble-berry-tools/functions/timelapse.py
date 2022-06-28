#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import os
import argparse
from datetime import datetime
from tqdm import tqdm


def make_timelapse(
    input_directory: str, output_directory: str, fps: int, video_format: str
) -> None:
    """make_timelapse allows to create a timelapse video from an input directory containing photos

    Args:
        input_directory (string): directory where are stored images used to create the video
        output_directory (string): directory where you need to save the final video
        fps (int): number of frame per seconds
    """
    print("#### Timelapse ####")
    l = []

    if os.path.isdir(input_directory) and os.path.isdir(output_directory):
        if input_directory[-1] != "/":
            input_directory = input_directory + "/"
        if output_directory[-1] != "/":
            output_directory = output_directory + "/"
    else:
        raise Exception("Either the input or ouput argument is not a directory")

    output_video = (
        output_directory
        + datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
        + "."
        + video_format
    )

    l = os.listdir(input_directory)
    l = sorted(l)
    height, width, layers = cv2.imread(input_directory + l[0]).shape

    if video_format == "avi":
        video = cv2.VideoWriter(
            output_video, cv2.VideoWriter_fourcc(*"MJPG"), fps, (width, height)
        )
    else:
        video = cv2.VideoWriter(
            output_video, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
        )

    for img_path in tqdm(l):
        video.write(cv2.imread(input_directory + img_path))

    cv2.destroyAllWindows()
    video.release()

    print("[\033[0;32m OK\033[0m ] ", output_video)
