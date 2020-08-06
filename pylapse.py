import cv2
import os

directory = './test/'
l = []
time_one_im = 0.2
fps = 1/time_one_im # may need a cast to int

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