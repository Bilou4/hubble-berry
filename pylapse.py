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
            print("processing image -> " + img_path)
            video.write(cv2.imread(directory + img_path))
        cv2.destroyAllWindows()
        video.release()
        print('video done')
    else:
        print('cannot find the directory - ' + directory)

def make_star_trail(directory):
    # TODO find a new operation different than average to make it brighter
    print('star trail')
    l = []
    step = 1
    output_image_path = "test.jpg"
    if os.path.exists(path=directory):
        l = os.listdir(directory)
        l = sorted(l)
        r, g, b = None, None, None
        r_avg, g_avg, b_avg = averager(), averager(), averager()

        count = 0
        for img_path in l:
            print("processing image -> " + img_path)

            # Split the frame into its respective channels
            frame = cv2.imread(directory + img_path)

            if count % step == 0 and frame is not None:
                # Get the current RGB
                b_curr, g_curr, r_curr = cv2.split(frame.astype("float"))
                r, g, b = r_avg(r_curr), g_avg(g_curr), b_avg(b_curr)
            
            count += 1

        # Merge the RGB averages together and write the output image to disk
        avg = cv2.merge([b, g, r]).astype("uint8")
        print("Saving image as ", output_image_path)
        cv2.imwrite(output_image_path, avg)

        cv2.destroyAllWindows()
            
    else:
        print('cannot find the directory - ' + directory)

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

parser = argparse.ArgumentParser()

parser.add_argument("-timelapse", help="If you want to create a timelapse", action="store_true")
parser.add_argument("-td", "--timelapse_input_directory", help="the input directory containing photos")
parser.add_argument("-t", "--time", help="time for the duration of a frame in the final video", type=float)

parser.add_argument("-startrail", help="If you want to create a startrail", action="store_true")
parser.add_argument("-sd", "--startrail_input_directory", help="the input directory containing photos")


args = parser.parse_args()
action_performed = False
if args.timelapse:
    if args.time is None or args.timelapse_input_directory is None:
        parser.error("To make a timelapse, you need to define an input directory and a time for each photo")
    directory = args.timelapse_input_directory
    time_one_im = args.time
    fps = 1/time_one_im # may need a cast to int
    make_timelapse(directory, fps)
    action_performed = True

if args.startrail:
    if args.startrail_input_directory is None:
        parser.error("To make a startrail, you need to define an input directory")
    directory = args.startrail_input_directory
    make_star_trail(directory)
    action_performed = True

if not action_performed:
    parser.error("You need to choose an action to perform, either timelapse or startrail or both.")