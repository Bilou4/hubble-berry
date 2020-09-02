#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import os
import argparse
from datetime import datetime
from tqdm import tqdm

def make_timelapse(input_directory, output_directory, fps, video_format):
    """make_timelapse allows to create a timelapse video from an input directory containing photos

    Args:
        input_directory (string): directory where are stored images used to create the video
        output_directory (string): directory where you need to save the final video
        fps (int): number of frame per seconds
    """
    print("#### Timelapse ####")
    l = []
    
    if os.path.isdir(input_directory) and os.path.isdir(output_directory):
        if input_directory[-1] != '/':
            input_directory = input_directory + '/'
        if output_directory[-1] != '/':
            output_directory = output_directory + '/'
    else:
        print("Either the input or ouput argument is not a directory")
        # TODO return ERROR
    
    output_video = output_directory + datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + '.' + video_format
    
    l = os.listdir(input_directory)
    l = sorted(l)
    height , width , layers =  cv2.imread(input_directory + l[0]).shape

    if video_format == 'avi':
        video = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*"MJPG"), fps, (width, height))
    else:
        video = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
        
    for img_path in tqdm(l):
        video.write(cv2.imread(input_directory + img_path))

    cv2.destroyAllWindows()
    video.release()
    
    print("[\033[0;32m OK\033[0m ] ", output_video)


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="the input directory containing photos")
parser.add_argument("-t", "--time", help="time for the duration of a frame in the final video", type=float)
parser.add_argument("-o", "--output", help="the output directory containing the final video")
parser.add_argument('--mp4', dest='format', action='store_const', const='mp4', default='avi', 
    help='The format you want for the video (default: avi)')


args = parser.parse_args()

if args.time is None or args.input is None or args.output is None:
    parser.error("To make a timelapse, you need to define an input & an output directory and a time for each photo")
input_directory = args.input
output_directory = args.output
time_one_im = args.time
fps = 1/time_one_im # may need a cast to int
make_timelapse(input_directory, output_directory, fps, args.format)

