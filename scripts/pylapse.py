#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import os
import argparse
from datetime import datetime
from tqdm import tqdm
import numpy

def make_timelapse(input_directory, output_directory, fps):
    """make_timelapse allows to create a timelapse video from an input directory containing photos

    Args:
        input_directory (string): directory where are stored images used to create the video
        output_directory (string): directory where you need to save the final video
        fps (int): number of frame per seconds
    """
    print("#### Timelapse ####")
    l = []
    
    if output_directory == '.':
        output_directory = './'
    
    output_video = output_directory + datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + '.avi'
    
    if os.path.exists(path=input_directory) and os.path.exists(path=output_directory):
        l = os.listdir(input_directory)
        l = sorted(l)
        height , width , layers =  cv2.imread(input_directory + l[0]).shape
        video = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*"MJPG"),
                                fps, (width, height))
        for img_path in tqdm(l):
            video.write(cv2.imread(input_directory + img_path))

        cv2.destroyAllWindows()
        video.release()
        
        print("[\033[0;32m OK\033[0m ] ", output_video)
    else:
        print("Cannot find the directory - ", input_directory)
        print("Or cannot find ", output_directory)

def make_star_trail_avg(input_directory, output_directory):
    """make_star_trail_avg allows to create a star trail based on the average method (make an average of pixel x,y from each image).

    Args:
       input_directory (string): directory where are stored images used to create the star trail
       output_directory (string): directory where you need to save the star trail
    """
    print("#### Star Trail Average ####")
    l = []
    step = 1

    if output_directory == '.':
        output_directory = './'
    
    output_image_path = output_directory + datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
    
    if os.path.exists(path=input_directory) and os.path.exists(path=output_directory):
        l = os.listdir(input_directory)
        l = sorted(l)
        r, g, b = None, None, None
        r_avg, g_avg, b_avg = averager(), averager(), averager()

        count = 0
        for img_path in tqdm(l):
            # Split the frame into its respective channels
            frame = cv2.imread(input_directory + img_path)

            if count % step == 0 and frame is not None:
                # Get the current RGB
                b_curr, g_curr, r_curr = cv2.split(frame.astype("float"))
                r, g, b = r_avg(r_curr), g_avg(g_curr), b_avg(b_curr)
            
            count += 1

        # Merge the RGB averages together and write the output image to disk
        avg = cv2.merge([b, g, r]).astype("uint8")
        cv2.imwrite(output_image_path, avg)
        cv2.destroyAllWindows()

        print("[\033[0;32m OK\033[0m ] ", output_image_path)
            
    else:
        print("Cannot find the directory - ", input_directory)
        print("Or cannot find ", output_directory)

def averager():
    """Calculate the average using a clojure."""
    count = 0
    total = 0.0

    def average(value):
        nonlocal count, total
        count += 1
        total += value
        return total / count

    return average

def make_star_trail_max(input_directory, output_directory):
    """make_star_trail_max allows to create a star trail based on the maximum method (keep the maximum value of pixel x,y from each image).

    Args:
       input_directory (string): directory where are stored images used to create the star trail
       output_directory (string): directory where you need to save the star trail
    """
    print("#### Star Trail Maximum value ####")
    l = []

    if output_directory == '.':
        output_directory = './'

    output_image_path = output_directory + datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
    
    if os.path.exists(path=input_directory) and os.path.exists(path=output_directory):
        l = os.listdir(input_directory)
        l = sorted(l)
        height, width, channel = cv2.imread(input_directory + l[0]).shape
        stack = numpy.zeros((height, width, 3), numpy.float)
        count = 1
        for img_path in tqdm(l):
            image_new = numpy.array(cv2.imread(input_directory + img_path), dtype = numpy.float)
            stack = numpy.maximum(stack, image_new)
            count += 1

        stack = numpy.array(numpy.round(stack), dtype = numpy.uint8)
        cv2.imwrite(output_image_path, stack)
        cv2.destroyAllWindows()

        print("[\033[0;32m OK\033[0m ] ", output_image_path)
            
    else:
        print("Cannot find the directory - ", input_directory)
        print("Or cannot find ", output_directory)



parser = argparse.ArgumentParser()

parser.add_argument("-timelapse", help="If you want to create a timelapse", action="store_true")
parser.add_argument("-ti", "--timelapse_input_directory", help="the input directory containing photos")
parser.add_argument("-t", "--time", help="time for the duration of a frame in the final video", type=float)
parser.add_argument("-to", "--timelapse_output_directory", help="the output directory containing the final video")


parser.add_argument("-startrail", help="If you want to create a startrail", action="store_true")
parser.add_argument("-si", "--startrail_input_directory", help="the input directory containing photos")
parser.add_argument("-so", "--startrail_output_directory", help="the output directory containing the final photo")
parser.add_argument('--avg', dest='method', action='store_const', const=make_star_trail_avg, default=make_star_trail_max, 
    help='method used to create the star trail (default: max)')

args = parser.parse_args()
action_performed = False
if args.timelapse:
    if args.time is None or args.timelapse_input_directory is None or args.timelapse_output_directory is None:
        parser.error("To make a timelapse, you need to define an input & an output directory and a time for each photo")
    input_directory = args.timelapse_input_directory
    output_directory = args.timelapse_output_directory
    time_one_im = args.time
    fps = 1/time_one_im # may need a cast to int
    make_timelapse(input_directory, output_directory, fps)
    action_performed = True

if args.startrail:
    if args.startrail_input_directory is None or args.startrail_output_directory is None:
        parser.error("To make a startrail, you need to define an input directory and an output directory")
    input_directory = args.startrail_input_directory
    output_directory = args.startrail_output_directory
    args.method(input_directory, output_directory) # call make_star_trail_avg or make_star_trail_max depending of the argument line
    action_performed = True

if not action_performed:
    parser.error("You need to choose an action to perform, either timelapse or startrail or both.")