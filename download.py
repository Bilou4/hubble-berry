#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from enum import Enum

class Action(Enum):
    COPY_PICTURES = 1
    COPY_TIMELAPSES = 2
    COPY_VIDEOS = 4
    MOVE_PICTURES = 8
    MOVE_TIMELAPSES = 16
    MOVE_VIDEOS = 32


def cp_pictures():
    print("cp_pictures")

def cp_timelapse():
    print("cp_timelapse")

def cp_videos():
    print("cp_videos")

def move_pictures():
    print("move_pictures")

def move_timelapse():
    print("move_timelapse")

def move_videos():
    print("move_videos")


parser = argparse.ArgumentParser()

parser.add_argument("-copy", help="If you want to copy files", action="store_true")
parser.add_argument("-move", help="If you want to move files", action="store_true")

parser.add_argument("-p", "--pictures", help="if your demand concerns pictures", action="store_true")
parser.add_argument("-t", "--timelapse", help="if your demand concerns timelapses", action="store_true")
parser.add_argument("-v", "--video", help="if your demand concerns videos", action="store_true")

args = parser.parse_args()
action_performed = False
action = 0

if args.copy:
    if not args.pictures and not args.timelapse and not args.video:
        parser.error("You need to specify at least one type of files to copy")
    else:
        action_performed = True
        if args.pictures:
            action = action | Action.COPY_PICTURES.value
        if args.timelapse:
            action = action | Action.COPY_TIMELAPSES.value
        if args.video:
            action = action | Action.COPY_VIDEOS.value

if args.move:
    if not args.pictures and not args.timelapse and not args.video:
        parser.error("You need to specify at least one type of files to move")
    else:
        action_performed = True
        if args.pictures:
            action = action | Action.MOVE_PICTURES.value
        if args.timelapse:
            action = action | Action.MOVE_TIMELAPSES.value
        if args.video:
            action = action | Action.MOVE_VIDEOS.value
        
if not action_performed:
    parser.error("You need to choose an action to perform, either copy or move files.")
else:
    if action & Action.COPY_PICTURES.value:
        cp_pictures()
    if action & Action.COPY_TIMELAPSES.value:
        cp_timelapse()
    if action & Action.COPY_VIDEOS.value:
        cp_videos()
    if action & Action.MOVE_PICTURES.value:
        move_pictures()
    if action & Action.MOVE_TIMELAPSES.value:
        move_timelapse()
    if action & Action.MOVE_VIDEOS.value:
        move_videos()