#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import cv2
import os
from datetime import datetime
from tqdm import tqdm


def make_timelapse(
    input_directory: Path, output_directory: Path, fps: int, video_format: str
) -> None:
    """make_timelapse allows to create a timelapse video from an input directory containing photos

    Args:
        input_directory (string): directory where are stored images used to create the video
        output_directory (string): directory where you need to save the final video
        fps (int): number of frame per seconds
    """
    print("#### Timelapse ####")
    files_list = []

    output_video = output_directory / str(
        datetime.today().strftime("%Y-%m-%d-%H-%M-%S") + "." + video_format
    )

    files_list = os.listdir(input_directory)
    files_list = sorted(files_list)
    height, width, layers = cv2.imread(input_directory / files_list[0]).shape

    if video_format == "avi":
        video = cv2.VideoWriter(
            output_video, cv2.VideoWriter_fourcc(*"MJPG"), fps, (width, height)
        )
    else:
        video = cv2.VideoWriter(
            output_video, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
        )

    for img_path in tqdm(files_list):
        video.write(cv2.imread(input_directory + img_path))

    cv2.destroyAllWindows()
    video.release()

    print("[\033[0;32m OK\033[0m ] ", output_video)
