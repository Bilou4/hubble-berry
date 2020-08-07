import cv2
import os
import argparse

def make_timelapse(directory, fps):
    print('timelapse')
    l = []
    if os.path.exists(path=directory):
        l = os.listdir(directory)
        l = sorted(l)
        height , width , layers =  cv2.imread(directory + l[0]).shape
        video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*"MJPG"),
                                fps, (width, height))
        for img_path in l:
            video.write(cv2.imread(directory + img_path))
        cv2.destroyAllWindows()
        video.release()
        print('video done')
    else:
        print('cannot find the directory - ' + directory)

def make_star_trail():
    print('star trail not implemented yet')
    
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="the directory containing photos for the timelapse", required=True)
parser.add_argument("-t", "--time", help="time for the duration of a frame in the final video", required=True, type=float)
parser.add_argument("-a", "--action", help="the action you want to perform", required=True)

args = parser.parse_args()
if(args.directory is not None and args.time is not None and args.action is not None):
    if (args.action not in ('startrail', 'timelapse', 'both')):
        parser.error("Only available actions are 'timelapse', 'startrail' or 'both'")
    directory = args.directory
    time_one_im = args.time
    fps = 1/time_one_im # may need a cast to int
    if (args.action == 'timelapse'):
        make_timelapse(directory, fps)
    elif (args.action == 'startrail'):
        make_star_trail()
    else:
        make_timelapse(directory, fps)
        make_star_trail()

