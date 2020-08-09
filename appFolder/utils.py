from appFolder import logger
import os
from fractions import Fraction
from time import sleep
from flask_babel import _
from shutil import move

try:
    import picamera
except:
    logger.error("No picamera module available")

picture_directory='./appFolder/static/camera/pictures/'
timelapse_directory='./appFolder/static/camera/timelapse/'
video_directory='./appFolder/static/camera/video/'

PROJECT_NAME = "Hubble-Berry"

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
        dict: contains a list of files that are in each folder
    """
    list_photos = sorted(os.listdir(picture_directory))
    list_photos.remove('do_not_remove.txt')
    list_timelapse = sorted(os.listdir(timelapse_directory))
    list_timelapse.remove('do_not_remove.txt')
    list_video = sorted(os.listdir(video_directory))
    list_video.remove('do_not_remove.txt')
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


def utils_take_photo(dic_elems):
    """Function using the picamera module to take a photo

    Args:
        dic_elems (dict): dictionnary containing values from form

    Returns:
        dict: text=a message to display to the User; 
                name=name of the pictures; 
                status=if something went wrong
    """
    try:
        if dic_elems['exposure_photo'] == 0:
            framerate = Fraction(0,1)
            picamera.PiCamera.CAPTURE_TIMEOUT = 60
        else:
            framerate = Fraction(1,dic_elems['exposure_photo'])
            picamera.PiCamera.CAPTURE_TIMEOUT = dic_elems['exposure_photo'] * 8 # environ à revoir

        with picamera.PiCamera(framerate=framerate) as camera:
            if dic_elems['resolution'] == (4056,3040):
                camera.sensor_mode = 3
            else:
                camera.sensor_mode = 0
            camera.shutter_speed = dic_elems['exposure_photo'] * 1000000
            camera.iso = dic_elems['iso']
            camera.resolution = dic_elems['resolution']
            if dic_elems['advanced_options_is_checked']:
                camera.brightness = dic_elems['brightness']
                camera.contrast = dic_elems['contrast']
                camera.sharpness = dic_elems['sharpness']
                camera.saturation = dic_elems['saturation']
                camera.rotation = dic_elems['rotation']
                camera.hflip = dic_elems['hflip']
                camera.vflip = dic_elems['vflip']
                camera.exposure_compensation = dic_elems['exposure_compensation']
                camera.exposure_mode = dic_elems['exposure_mode']
                camera.image_effect = dic_elems['image_effect']
                camera.meter_mode = dic_elems['meter_mode']
                camera.awb_mode = dic_elems['awb_mode']
            add_exif_tags(camera) # TODO: check if exif tags is working with format other than jpg
            logger.info('Camera set up')
            if dic_elems['exposure_photo'] > 6:
                sleep(30) # warmup
            else:
                sleep(3)
            logger.info('End of camera warmup')
            if dic_elems['file_format'] == 'jpg':
                file_format_bis = 'jpeg'
            else:
                file_format_bis = dic_elems['file_format']
            camera.capture(picture_directory + dic_elems['photo_name'] + '.' + dic_elems['file_format'], format=file_format_bis)
            logger.info('The photo was taken')
            camera.shutter_speed = 0
            camera.framerate = 1
        logger.info('Everything is closed, sending back the response')
        return {'text': _("Photo was taken!"), 'name':dic_elems['photo_name'], 'status':"ok"}
    except Exception as e:
        message_error = "[utils_take_photo] " + str(e)
        logger.error(message_error)
        return {'text': message_error, 'name':"", 'status':"error"}

def utils_take_timelapse(dic_elems):
    """Function using the picamera module to take a timelapse

    Args:
        dic_elems (dict): dictionnary containing values from form

    Returns:
        dict: text=a message to display to the User; 
                status=if something went wrong
    """
    try:
        if dic_elems['exposure_photo'] == 0:
            framerate = Fraction(0,1)
        else:
            framerate = Fraction(1, dic_elems['exposure_photo'])
        with picamera.PiCamera(framerate=framerate) as camera:
            if dic_elems['resolution'] == (4056,3040):
                camera.sensor_mode = 3
            else:
                camera.sensor_mode = 0
            camera.resolution = dic_elems['resolution']
            camera.shutter_speed = dic_elems['exposure_photo'] * 1000000
            add_exif_tags(camera)
            vide_port = dic_elems['use_video_port_checkbox']
            logger.info('Camera set up')
            if dic_elems['exposure_photo'] > 6:
                sleep(30) # warmup
            else:
                sleep(3)
            logger.info('End of camera warmup')
            for i, filename in enumerate(camera.capture_continuous(timelapse_directory+'{timestamp:%Y_%m_%d_%H_%M_%S}-{counter:03d}.jpg', format='jpeg', use_video_port=vide_port)):
                logger.info('I took a photo => ' + filename)
                if i == dic_elems['number_photos']-1:
                    break
                sleep(dic_elems['time_between_photos'] - dic_elems['exposure_photo'])
            camera.shutter_speed = 0
            camera.framerate = 1
        logger.info('Everything is closed, sending back the response')
        return {'text': _("Timelapse is over"), 'status':"ok"}
    except Exception as e:
        message_error = "[utils_take_timelapse] " + str(e)
        logger.error(message_error)
        return {'text': message_error, 'status':"error"}

def utils_take_video(dic_elems):
    """Function using the picamera module to take a video

    Args:
        dic_elems (dict): dictionnary containing values from form

    Returns:
        dict: text=a message to display to the User; 
                name=name of the pictures; 
                status=if something went wrong
    """
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = dic_elems['resolution']
            logger.info('Camera set up')
            sleep(2) # warmup
            logger.info('End of camera warmup')
            camera.start_recording(video_directory + dic_elems['video_name'] + ".h264", format='h264')
            camera.wait_recording(dic_elems['video_time'])
            camera.stop_recording()
        logger.info('Everything is closed, sending back the response')
        return {'text': _("Video is over"), 'name': dic_elems['video_name'], 'status':"ok"}
    except Exception as e:
        message_error = "[utils_take_video] " + str(e)
        logger.error(message_error)
        return {'text':message_error, 'name':"", 'status':"error"}