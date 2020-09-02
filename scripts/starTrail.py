#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import os
import argparse
from datetime import datetime
from tqdm import tqdm
import numpy

def make_star_trail_avg(input_directory, output_directory):
    """make_star_trail_avg allows to create a star trail based on the average method (make an average of pixel x,y from each image).

    Args:
       input_directory (string): directory where are stored images used to create the star trail
       output_directory (string): directory where you need to save the star trail
    """
    print("#### Star Trail Average ####")
    l = []
    step = 1

    if os.path.isdir(path=input_directory) and os.path.isdir(path=output_directory):
        if input_directory[-1] != '/':
            input_directory = input_directory + '/'
        if output_directory[-1] != '/':
            output_directory = output_directory + '/'
    else:
        print("Either the input or ouput argument is not a directory")
        # TODO return ERROR

    output_image_path = output_directory + datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
    
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

    if os.path.isdir(input_directory) and os.path.isdir(output_directory):
        if input_directory[-1] != '/':
            input_directory = input_directory + '/'
        if output_directory[-1] != '/':
            output_directory = output_directory + '/'
    else:
        print("Either the input or ouput argument is not a directory")
        # TODO return ERROR - FileNotFoundError - NotADirectoryError

    output_image_path = output_directory + datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
    
    l = os.listdir(input_directory)
    l = sorted(l)
    height, width, channel = cv2.imread(input_directory + l[0]).shape
    stack = numpy.zeros((height, width, 3), numpy.float)
    for img_path in tqdm(l):
        image_new = numpy.array(cv2.imread(input_directory + img_path), dtype = numpy.float)
        stack = numpy.maximum(stack, image_new)

    stack = numpy.array(numpy.round(stack), dtype = numpy.uint8)
    cv2.imwrite(output_image_path, stack)
    cv2.destroyAllWindows()

    print("[\033[0;32m OK\033[0m ] ", output_image_path)


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="the input directory containing photos")
parser.add_argument("-o", "--output", help="the output directory containing the final photo")
parser.add_argument('--avg', dest='method', action='store_const', const=make_star_trail_avg, default=make_star_trail_max, 
    help='method used to create the star trail (default: max)')

args = parser.parse_args()

if args.input is None or args.output is None:
    parser.error("To make a startrail, you need to define an input directory and an output directory")
input_directory = args.input
output_directory = args.output
args.method(input_directory, output_directory) # call make_star_trail_avg or make_star_trail_max depending of the argument line
