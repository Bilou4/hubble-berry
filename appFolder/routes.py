from appFolder import app, db
from appFolder.models import User, Role
from appFolder.forms import LoginForm, RegistrationForm

from flask import render_template, flash, redirect,\
     url_for, request, Response
from flask_login import current_user, login_user, logout_user,\
    login_required
from werkzeug.urls import url_parse

from datetime import datetime
from appFolder.camera import Camera
from shutil import copyfile, move
import os
# import picamera
from time import sleep


PROJECT_NAME = 'Hubble-Berry'
picture_directory="./appFolder/static/camera/pictures/"
timelapse_directory="./appFolder/static/camera/timelapse/"
video_directory="./appFolder/static/camera/video/"

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
    return render_template('index.html', title=PROJECT_NAME + '- Index')

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
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '': # empecher l'utilisateur de rediriger vers un site malicieux
            next_page = url_for('preview')
        return redirect(next_page)
    return render_template('login.html', title=PROJECT_NAME + '- Sign In', form=form)

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
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title=PROJECT_NAME + '- Register', form=form)


@app.route('/functionalities', methods=['GET','POST'])
@login_required
def functionalities():
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    if user_role[0] == 'admin':
        return render_template('functionalities.html', title=PROJECT_NAME + '- Direct')
    else:
        return redirect(url_for('preview'))
        
@app.route('/preview')
@login_required
def preview():
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    return render_template("preview.html", title=PROJECT_NAME + '- Preview', role=user_role[0])

@app.route('/gallery')
@login_required
def gallery():
    dic_of_files = get_dic_of_files()
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    return render_template("gallery.html", title=PROJECT_NAME + '- Gallery', 
            role=user_role[0], photo_files=dic_of_files["photos"], 
            timelapse_file=dic_of_files["timelapse"], video_file=dic_of_files["video"])

@app.errorhandler(404)
def page_not_found(error):
    # note that we set the 404 status explicitly
    return render_template('404.html', title=PROJECT_NAME + '- ERROR'), 404

@app.route('/take_a_photo', methods=['POST'])
@login_required
def take_a_photo():
    photo_name = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    #exposure_photo = int(request.form['exposure_photo'])
    # cannot use python boolean type because the request sent a string
    try:
        with picamera.PiCamera() as camera:
            #camera.shutter_speed = exposure_photo
            #camera.iso = 
            camera.resolution = (1920,1080)
            sleep(2) # warmup
            camera.capture(picture_directory+photo_name+'.png',format='png')
        return {"text":"photo prise!","name":photo_name, "status":"ok"}
    except Exception as e:
        message_error = "[ERROR] " + e
        return {"text": message_error, "name":"NULL", "status":"error"}


@app.route('/take_timelapse', methods=['POST'])
@login_required
def take_timelapse():
    exposure_photo = float(request.form['exposure_photo'])
    time_between_photos = float(request.form['time_between_photos'])
    number_photos = int(request.form['number_photos'])
    print(time_between_photos)
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            #camera.shutter_speed = exposure_photo / 1000000 # from secondes to microseconds
            sleep(2) # warmup
            for i, filename in enumerate(camera.capture_continuous(timelapse_directory+'{timestamp:%Y_%m_%d_%H_%M_%S}-{counter:03d}.png',use_video_port=True)):
                print(filename)
                sleep(time_between_photos-3.0)
                if i == number_photos-1:
                    break
        return {"text":"Timelapse terminé","name": datetime.today().strftime('%Y-%m-%d-%H-%M-%S'), "status":"ok"}
    except Exception as e:
        message_error = "[ERROR] " + e
        return {"text": message_error, "name":"NULL", "status":"error"}



@app.route('/start_video', methods=['POST'])
@login_required
def start_video():
    video_time = int(request.form['video_time'])
    video_name = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    try:
        with picamera.PiCamera() as camera:
            sleep(2) # warmup
            camera.start_recording(video_directory+video_name+".h264",format='h264')
            camera.wait_recording(video_time)
            camera.stop_recording()
        return {"text":"Vidéo terminée","name": video_name, "status":"ok"}
    except Exception as e:
        message_error = "[ERROR] " + e
        return {"text":message_error, "name":"NULL", "status":"error"}

@app.route('/get_dic_of_files')
@login_required
def get_dic_of_files():
    return {"photos":os.listdir(picture_directory),
            "timelapse":os.listdir(timelapse_directory),
            "video":os.listdir(video_directory)}

@app.route('/save_usb', methods=['POST'])
@login_required
def save_usb():
    path_to_usb = "/media/pi/HUBBLE_SAVE/camera/"
    if os.path.exists(path=path_to_usb):
        move_files(picture_directory, path_to_usb+'pictures')
        move_files(timelapse_directory, path_to_usb+'timelapse')
        move_files(video_directory, path_to_usb+'video')
        return {"text": "fichiers transférés"}
    else:
        return {"text": "Aucune clé trouvée"}

def move_files(src, dst):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        move(src=s, dst=d)

# TODO ==> camera integration
# The Raspberry Pi High Quality Camera’s maximum resolution is 4056 x 3040 pixels
# (5K) and this produces an image of around 6MB in size. 
# Images are typically saved as JPG, but we can also select
#    RAW, GIF, BMP, PNG, YUV420, RG8888 file formats.
#
# https://picamera.readthedocs.io/en/release-1.13/api_camera.html#piframeraterange

"""
ISO = 800 || 1600 si shutter = 1/60 ||
brightness
contrast (increase noise)


video, best = 1080p at 30 fps

camera.brightness = 50 (0 to 100)
camera.sharpness = 0 (-100 to 100)
camera.contrast = 0 (-100 to 100)
camera.saturation = 0 (-100 to 100)
camera.iso = 0 (auto), 100, 200, 320, 400, 500, 640, or 800.
camera.exposure_compensation = 0 (-25 to 25)
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.rotation = 0
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)

camera.resolution = (1024, 768)
4056 × 3040
2028 × 1520
2028 × 1080
1012 × 760
The maximum resolution for photos is 4056 × 3040 (HQ Camera)

camera.image_effect = [none (the default), negative,
solarize, sketch, denoise, emboss, oilpaint, hatch, gpen (graphite sketch effect), pastel,
watercolor, film, blur, saturation, colorswap, washedout, posterise, colorpoint,
colorbalance, cartoon, deinterlace1, deinterlace2]

exposure_mode = ['off', 'auto' (default),
'night', 'nightpreview', 'backlight', 'spotlight', 'sports', 'snow', 'beach',
'verylong', 'fixedfps', 'antishake', 'fireworks'.]
"""


"""3.7. Capturing in low light
from picamera import PiCamera
from time import sleep
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
# TODO ==> add conf elements
# TODO ==> cf splitter (plusieurs ports)
# TODO pictures => quality
# TODO gallery => chargement des images