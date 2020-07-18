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
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('preview'))
    return render_template('index.html', title=PROJECT_NAME + _("- Index"))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('preview'))
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
            next_page = url_for('preview')
        return redirect(next_page)
    return render_template('login.html', title=PROJECT_NAME + _("- Sign In"), form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
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
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    if user_role[0] == 'admin':
        return render_template('functionalities.html', title=PROJECT_NAME + _("- Direct"), role=user_role[0])
    else:
        return redirect(url_for('preview'))
        
@app.route('/preview')
@login_required
def preview():
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    return render_template("preview.html", title=PROJECT_NAME + _("- Preview"), role=user_role[0])

@app.route('/gallery')
@login_required
def gallery():
    dic_of_files = get_dic_of_files()
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    return render_template("gallery.html", title=PROJECT_NAME + _("- Gallery"), 
            role=user_role[0], photo_file=dic_of_files['photos'], 
            timelapse_file=dic_of_files['timelapse'], video_file=dic_of_files['video'])

@app.errorhandler(404)
def page_not_found(error):
    # note that we set the 404 status explicitly
    return render_template('404.html', title=PROJECT_NAME + _("- ERROR")), 404

@app.route('/take_a_photo', methods=['POST'])
@login_required
def take_a_photo():
    photo_name = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    exposure_photo = int(float(request.form['exposure_photo'].replace(',','.')))
    resolution = (int(request.form['resolution_photo'].split(',')[0]), int(request.form['resolution_photo'].split(',')[1]))
    iso = int(request.form['iso_photo'])
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
    logger.info('Retrieved information from form')
    try:
        with picamera.PiCamera(framerate=Fraction(1,exposure_photo)) as camera:
            camera.sensor_mode = 3
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
                # camera.sensor_mode    https://medium.com/@alexellisuk/in-depth-review-and-comparison-of-the-raspberry-pi-high-quality-camera-806490c4aeb7    
            add_exif_tags(camera)
            picamera.PiCamera.CAPTURE_TIMEOUT = exposure_photo * 8 # environ à revoir
            logger.info('Camera set up')
            sleep(30) # warmup
            logger.info('End of camera warmup')
            camera.capture(picture_directory+photo_name+'.jpg',format='jpeg')
            logger.info('The photo was taken')
            camera.shutter_speed = 0
            camera.framerate = 1
        logger.info('Everything is closed, sending back the response')
        return {'text': _("Photo was taken!"), 'name':photo_name, 'status':"ok"}
    except Exception as e:
        message_error = "[ERROR] " + str(e)
        logger.error(message_error)
        return {'text': message_error, 'name':"NULL", 'status':"error"}


@app.route('/take_timelapse', methods=['POST'])
@login_required
def take_timelapse():
    exposure_photo = int(float(request.form['exposure_photo'].replace(',','.')))
    time_between_photos = int(float(request.form['time_between_photos'].replace(',','.')))
    number_photos = int(float(request.form['number_photos'].replace(',','.')))
    resolution = (int(request.form['resolution_timelapse'].split(',')[0]), int(request.form['resolution_timelapse'].split(',')[1]))
    iso = int(request.form['iso_timelapse'])
    logger.info('Retrieved information from form')
    try:
        with picamera.PiCamera(framerate=Fraction(1,exposure_photo)) as camera:
            camera.sensor_mode = 3
            camera.resolution = resolution
            camera.shutter_speed = exposure_photo * 1000000
            logger.info('Camera set up')
            sleep(30) # warmup
            logger.info('End of camera warmup')
            for i, filename in enumerate(camera.capture_continuous(timelapse_directory+'{timestamp:%Y_%m_%d_%H_%M_%S}-{counter:03d}.jpg', format='jpeg', use_video_port=True)):
                logger.info('I took a photo => ' + filename)
                if i == number_photos-1:
                    break
                sleep(time_between_photos)
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
    video_time = int(float(request.form['video_time'].replace(',','.')))
    video_name = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    resolution = (int(request.form['resolution_video'].split(',')[0]),int(request.form['resolution_video'].split(',')[1]))
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
    camera.exif_tags['IFD0.Artist'] = PROJECT_NAME
    camera.exif_tags['IFD0.Copyright'] = "Copyright (c) 2020 " + PROJECT_NAME

def get_dic_of_files():
    return {'photos': sorted(os.listdir(picture_directory)),
            'timelapse':sorted(os.listdir(timelapse_directory)),
            'video':sorted(os.listdir(video_directory))}

@app.route('/save_usb', methods=['POST'])
@login_required
def save_usb():
    path_to_usb = "/media/pi/HUBBLE_SAVE/camera/"
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
    return render_template("messier.html", title=PROJECT_NAME + _("- Messier's catalog"))


def move_files(src, dst):
    for item in os.listdir(src):
        if item != "do_not_remove.txt":
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            move(src=s, dst=d)

# TODO ==> camera integration
# https://picamera.readthedocs.io/en/release-1.13/api_camera.html#piframeraterange

"""
camera.crop = (0.0, 0.0, 1.0, 1.0)
"""


"""3.7. Capturing in low light
from fractions import Fraction

# Force sensor mode 3 (the long exposure mode), set
# the framerate to 1/6fps, the shutter speed to 6s,
# and ISO to 800 (for maximum gain)

camera = PiCamera(
    resolution=(1280, 720),
    framerate=Fraction(1, 6),
    sensor_mode=3)
camera.shutter_speed = 6000000
camera.iso = 800

# Give the camera a good long time to set gains and
# measure AWB (you may wish to use fixed AWB instead)

sleep(30)
camera.exposure_mode = 'off'

# Finally, capture an image with a 6s exposure. Due
# to mode switching on the still port, this will take
# longer than 6 seconds

camera.capture('dark.jpg')

"""
# TODO ==> cf splitter (plusieurs ports)
# TODO ==> TESTS
# TODO ==> languages

"""
https://picamera.readthedocs.io/en/latest/fov.html#hardware-limits

sudo vcgencmd get_camera
==> supported=1 detected=1

raspistill -v -o test.jpg

"""
