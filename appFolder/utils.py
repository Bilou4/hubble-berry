import os

picture_directory='./appFolder/static/camera/pictures/'
timelapse_directory='./appFolder/static/camera/timelapse/'
video_directory='./appFolder/static/camera/video/'


def gen(camera):
    """It enters a loop where it continuously returns frames from 
        the camera as response chunks. The function asks the camera 
        to provide a frame by calling the camera.get_frame() method, and 
        then it yields with this frame formatted as a response chunk with a content 
        type of image/jpeg

    Args:
        camera (picamera.PiCamera): An instance of the camera class

    Yields:
        bytes: content type of image/jpeg
    """
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def add_exif_tags(camera):
    """Function used to add some exif tags on each photos.

    Args:
        camera (picamera.PiCamera): the camera object on which exif tag are needed
    """
    camera.exif_tags['IFD0.Artist'] = PROJECT_NAME
    camera.exif_tags['IFD0.Copyright'] = "Copyright (c) 2020 " + PROJECT_NAME

def get_dic_of_files():
    """Function to retrieve files in picture, timelapse and video folder

    Returns:
        dictionnary: contains a list of files that are in each folder
    """
    list_photos = sorted(os.listdir(picture_directory))
    list_photos.remove('do_not_remove.txt')
    list_timelapse = sorted(os.listdir(timelapse_directory))
    list_timelapse.remove('do_not_remove.txt')
    list_video = sorted(os.listdir(video_directory))
    list_video.remove('do_not_remove.txt')
    #TODO: remove the path of 'do_not_remove.txt' file .remove() ==> avoid doing this in web page
    return {'photos': list_photos,
            'timelapse': list_timelapse,
            'video': list_video}

def move_files(src, dst):
    """Move files between source and destination

    Args:
        src (string): The source path of files to move
        dst (string): The destination path of files to move
    """
    for item in os.listdir(src):
        if item != "do_not_remove.txt":
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            move(src=s, dst=d)
