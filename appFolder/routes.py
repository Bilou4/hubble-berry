from appFolder import app, db, logger
from appFolder.models import User, Role
from appFolder.forms import LoginForm, RegistrationForm

from flask import render_template, flash, redirect,\
     url_for, request, Response
from flask_login import current_user, login_user, logout_user,\
    login_required
from werkzeug.urls import url_parse
from flask_babel import _

from datetime import datetime
from shutil import copyfile, move
import os
from fractions import Fraction
try:
    from appFolder.camera_pi import Camera
    import picamera
except:
    from appFolder.camera import Camera
from time import sleep


PROJECT_NAME = "Hubble-Berry"
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

@app.route('/video_feed')
def video_feed():
    """This stream returns the images that are going to be displayed in the web page

    Returns:
        Response: The streaming response
    """
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
@app.route('/index')
def index():
    """Render the default page for the User

    Returns:
        template: the default template according if the user is connected or not
    """
    if current_user.is_authenticated:
        return redirect(url_for('preview'))
    return render_template('index.html', title=PROJECT_NAME + _("- Index"))

@app.route('/logout')
def logout():
    """Function to logout a user

    Returns:
        template: Returns to the default page
    """
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Function to sign in the User

    Returns:
        template: The login page if he is not already connected or the index page
    """
    if current_user.is_authenticated:
        return redirect(url_for('preview')) # TODO: change to index
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_("Invalid username or password"))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        logger.info(user.username + ' is now connected')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '': # empecher l'utilisateur de rediriger vers un site malicieux
            next_page = url_for('preview') # TODO: change to index
        return redirect(next_page)
    return render_template('login.html', title=PROJECT_NAME + _("- Sign In"), form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Function to allow a new User to register

    Returns:
        template: The register page or the login page if the registration went well
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.set_default_role()
        db.session.add(user)
        db.session.commit()
        logger.info('A new user is registered => ', user.username)
        flash(_("Congratulations, you are now a registered user!"))
        return redirect(url_for('login'))
    return render_template('register.html', title=PROJECT_NAME + _("- Register"), form=form)


@app.route('/functionalities', methods=['GET','POST'])
@login_required
def functionalities():
    """Function to redirect to the functionnalities page

    Returns:
        template: If the User is an admin, he can access the page
    """
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    if user_role[0] == 'admin':
        return render_template('functionalities.html', title=PROJECT_NAME + _("- Direct"), role=user_role[0])
    else:
        return redirect(url_for('preview'))
        
@app.route('/preview')
@login_required
def preview():
    """Function to redirect to the preview page

    Returns:
        template: Any user can access the preview page
    """
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    return render_template("preview.html", title=PROJECT_NAME + _("- Preview"), role=user_role[0])

@app.route('/gallery')
@login_required
def gallery():
    """Function to redirect to the gallery page

    Returns:
        template: Send all pictures, timelapse and videos to the page
    """
    dic_of_files = get_dic_of_files()
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    return render_template("gallery.html", title=PROJECT_NAME + _("- Gallery"), 
            role=user_role[0], photo_file=dic_of_files['photos'], 
            timelapse_file=dic_of_files['timelapse'], video_file=dic_of_files['video'])

@app.errorhandler(404)
def page_not_found(error):
    """Function to redirect to a 404 error page

    Args:
        error (404): The server did not find the requested resource. 

    Returns:
        template: The default 404 page
    """
    # note that we set the 404 status explicitly
    return render_template('404.html', title=PROJECT_NAME + _("- ERROR")), 404

@app.route('/take_a_photo', methods=['POST'])
@login_required
def take_a_photo():
    """Function to take a photo with the Rpi camera

    Returns:
        dictionnary: text=a message to display to the User; name=name of the pictures; status=if something went wrong
    """
    try:
        photo_name = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        exposure_photo = int(float(request.form['exposure_photo'].replace(',','.')))
        resolution = (int(request.form['resolution_photo'].split(',')[0]), int(request.form['resolution_photo'].split(',')[1]))
        iso = int(request.form['iso_photo'])
        file_format = request.form['format_photo']
        advanced_options_is_checked = True if request.form['advanced_options_checkbox']=='true' else False
        if advanced_options_is_checked:
            brightness = int(float(request.form['brightness_photo'].replace(',','.')))
            contrast = int(float(request.form['contrast_photo'].replace(',','.')))
            sharpness = int(float(request.form['sharpness_photo'].replace(',','.')))
            saturation = int(request.form['saturation_photo'])
            rotation = int(float(request.form['rotation_photo'].replace(',','.')))
            hflip = True if request.form['hflip_photo']=='true' else False
            vflip = True if request.form['vflip_photo']=='true' else False
            exposure_compensation = int(float(request.form['exposure_compensation_photo'].replace(',','.')))
            exposure_mode = request.form['exposure_mode_photo']
            image_effect = request.form['image_effect_photo']
            meter_mode = request.form['meter_mode_photo']
            awb_mode = request.form['awb_mode_photo']
    except Exception as e:
        message_error = "[ERROR] " + str(e)
        logger.error(message_error)
        return {'text': message_error, 'name':"NULL", 'status':"error"}

    logger.info('Retrieved information from form')
    try:
        if exposure_photo == 0:
            framerate = Fraction(0,1)
            picamera.PiCamera.CAPTURE_TIMEOUT = 60
        else:
            framerate = Fraction(1,exposure_photo)
            picamera.PiCamera.CAPTURE_TIMEOUT = exposure_photo * 8 # environ à revoir

        with picamera.PiCamera(framerate=framerate) as camera:
            if resolution == (4056,3040):
                camera.sensor_mode = 3
            else:
                camera.sensor_mode = 0
            camera.shutter_speed = exposure_photo * 1000000
            camera.iso = iso
            camera.resolution = resolution
            if advanced_options_is_checked:
                camera.brightness = brightness
                camera.contrast = contrast
                camera.sharpness = sharpness
                camera.saturation = saturation
                camera.rotation = rotation
                camera.hflip = hflip
                camera.vflip = vflip
                camera.exposure_compensation = exposure_compensation
                camera.exposure_mode = exposure_mode
                camera.image_effect = image_effect
                camera.meter_mode = meter_mode
                camera.awb_mode = awb_mode
            add_exif_tags(camera) # TODO: check if exif tags is working with format other than jpg
            logger.info('Camera set up')
            if exposure_photo > 10:
                sleep(30) # warmup
            else:
                sleep(3)
            logger.info('End of camera warmup')
            if file_format == 'jpg':
                file_format_bis = 'jpeg'
            else:
                file_format_bis = file_format
            camera.capture(picture_directory + photo_name + '.' + file_format, format=file_format_bis)
            logger.info('The photo was taken')
            camera.shutter_speed = 0
            camera.framerate = 1
        logger.info('Everything is closed, sending back the response')
        return {'text': _("Photo was taken!"), 'name':photo_name, 'status':"ok"}
    except Exception as e:
        message_error = "[ERROR] " + str(e)
        logger.error(message_error)
        return {'text': message_error, 'name':"NULL", 'status':"error"}

# TODO: Make something with the name return in the response
@app.route('/take_timelapse', methods=['POST'])
@login_required
def take_timelapse():
    """Function to take a timelapse with the Rpi camera

    Returns:
        dictionnary: text=a message to display to the User; name=datetime when timelapse is over; status=if something went wrong
     """
    try:
        exposure_photo = int(float(request.form['exposure_photo'].replace(',','.')))
        time_between_photos = int(float(request.form['time_between_photos'].replace(',','.')))
        number_photos = int(float(request.form['number_photos'].replace(',','.')))
        resolution = (int(request.form['resolution_timelapse'].split(',')[0]), int(request.form['resolution_timelapse'].split(',')[1]))
        iso = int(request.form['iso_timelapse'])
    except Exception as e:
        message_error = "[ERROR] " + str(e)
        logger.error(message_error)
        return {'text': message_error, 'name':"NULL", 'status':"error"}

    logger.info('Retrieved information from form')
    try:
        if exposure_photo == 0:
            framerate = Fraction(0,1)
        else:
            framerate = Fraction(1,exposure_photo)
        with picamera.PiCamera(framerate=framerate) as camera:
            if resolution == (4056,3040):
                camera.sensor_mode = 3
            else:
                camera.sensor_mode = 0
            camera.resolution = resolution
            camera.shutter_speed = exposure_photo * 1000000
            add_exif_tags(camera)
            logger.info('Camera set up')
            if exposure_photo > 10:
                sleep(30) # warmup
            else:
                sleep(3)
            logger.info('End of camera warmup')
            # TODO : essayer sans use_port_video
            for i, filename in enumerate(camera.capture_continuous(timelapse_directory+'{timestamp:%Y_%m_%d_%H_%M_%S}-{counter:03d}.jpg', format='jpeg', use_video_port=True)):
                logger.info('I took a photo => ' + filename)
                if i == number_photos-1:
                    break
                sleep(time_between_photos - exposure_photo) # essaie en enlevant le temps d'exposition
            camera.shutter_speed = 0
            camera.framerate = 1
        logger.info('Everything is closed, sending back the response')
        return {'text': _("Timelapse is over"), 'name': datetime.today().strftime('%Y-%m-%d-%H-%M-%S'), 'status':"ok"}
    except Exception as e:
        message_error = "[ERROR] " + str(e)
        logger.error(message_error)
        return {'text': message_error, 'name':"NULL", 'status':"error"}



@app.route('/start_video', methods=['POST'])
@login_required
def start_video():
    """Function to take a video with the Rpi camera

    Returns:
        dictionnary: text=a message to display to the User; name=video name; status=if something went wrong
      """
    try:
        video_time = int(float(request.form['video_time'].replace(',','.')))
        video_name = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        resolution = (int(request.form['resolution_video'].split(',')[0]),int(request.form['resolution_video'].split(',')[1]))
    except Exception as e:
        message_error = "[ERROR] " + str(e)
        logger.error(message_error)
        return {'text': message_error, 'name':"NULL", 'status':"error"}

    logger.info('Retrieved information from form')
    try:
        with picamera.PiCamera() as camera:
            logger.info('Camera set up')
            sleep(2) # warmup
            logger.info('End of camera warmup')
            camera.start_recording(video_directory+video_name+".h264",format='h264')
            camera.wait_recording(video_time)
            camera.stop_recording()
        logger.info('Everything is closed, sending back the response')
        return {'text': _("Video is over"), 'name': video_name, 'status':"ok"}
    except Exception as e:
        message_error = "[ERROR] " + str(e)
        logger.error(message_error)
        return {'text':message_error, 'name':"NULL", 'status':"error"}

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
    #TODO: remove the path of 'do_not_remove.txt' file .remove() ==> avoid doing this in web page
    return {'photos': sorted(os.listdir(picture_directory)),
            'timelapse':sorted(os.listdir(timelapse_directory)),
            'video':sorted(os.listdir(video_directory))}

@app.route('/save_usb', methods=['POST'])
@login_required
def save_usb():
    """Function to save files in the USB key

    Returns:
        dictionnary: text=a message to inform the User
    """
    path_to_usb = "/media/pi/HUBBLE_SAVE/camera/"
    # TODO: check for possibility to mount the usb key
    if os.path.exists(path=path_to_usb):
        move_files(picture_directory, path_to_usb+'pictures')
        logger.info('I moved pictures')
        move_files(timelapse_directory, path_to_usb+'timelapse')
        logger.info('I moved timelapse')
        move_files(video_directory, path_to_usb+'video')
        logger.info('I moved video')
        return {'text': _("Files have been transferred")}
    else:
        return {'text': _("No USB key detected")}

@app.route('/messier')
@login_required
def messier():
    """Function to render the messier's catalog page

    Returns:
        template: The messier web page
    """
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    return render_template("messier.html", title=PROJECT_NAME + _("- Messier's catalog"), role=user_role[0])


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

# TODO ==> camera integration
# https://picamera.readthedocs.io/en/release-1.13/api_camera.html#piframeraterange

# TODO ==> cf splitter (plusieurs ports)

