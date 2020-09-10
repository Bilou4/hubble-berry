#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import os
import argparse
import mimetypes

def is_a_video(input_file):
    mimetypes.init()
    mimestart = mimetypes.guess_type(input_file)[0]
    if mimestart != None:
        mimestart = mimestart.split('/')[0]
        if mimestart == 'video':
            return True
    return False

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="the input video")
parser.add_argument("-o", "--output", help="the output folder that will contain the images from the video")

args = parser.parse_args()

if args.input is None or args.output is None:
    parser.error("To extract images from a video, you need to specify an input video & an output directory")
input_file = args.input
output_directory = args.output

if is_a_video(input_file) and os.path.isdir(output_directory):
    if output_directory[-1] != '/':
        output_directory = output_directory + '/'
else:
    raise Exception("Either the input is not a video file or the output is not a directory")

cap = cv2.VideoCapture(input_file)
count = 0
while cap.isOpened():
    ret,frame = cap.read()
    #cv2.imshow('window-name',frame)
    cv2.imwrite(output_directory + 'frame%d.jpg' % count, frame)
    count = count + 1
    if cv2.waitKey(10) & 0xFF == ord('q'): # press q to exit the program
        break


cap.release()
cv2.destroyAllWindows()  # destroy all the opened windows

