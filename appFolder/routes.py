from appFolder import app, db
from appFolder.models import User, Role
from appFolder.forms import LoginForm, RegistrationForm

from flask import render_template, flash, redirect,\
     url_for, request, Response
from flask_login import current_user, login_user, logout_user,\
    login_required
from werkzeug.urls import url_parse

from datetime import datetime
from appFolder.camera_pi import Camera
from shutil import copyfile, move
import os
import picamera
from time import sleep


PROJECT_NAME = 'Hubble-Berry'


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
            sleep(2)
            camera.capture('./camera/pictures/'+photo_name,format='png')
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
            sleep(2)
            for i, filename in enumerate(camera.capture_continuous('./camera/timelapse/{timestamp:%Y_%m_%d_%H_%M_%S}-{counter:03d}.png',use_video_port=True)):
                print(filename)
                sleep(time_between_photos)
                if i == number_photos:
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
            camera.start_recording("./camera/video/"+video_name,format='h264')
            camera.wait_recording(video_time)
            camera.stop_recording()
        return {"text":"Vidéo terminée","name": video_name, "status":"ok"}
    except Exception as e:
        message_error = "[ERROR] " + e
        return {"text":message_error, "name":"NULL", "status":"error"}


@app.route('/save_usb', methods=['POST'])
@login_required
def save_usb():
    path_to_usb = "/media/pi/HUBBLE_SAVE/camera/"
    if os.path.exists(path=path_to_usb):
        move_files('./camera/pictures/', path_to_usb+'pictures')
        move_files('./camera/timelapse/', path_to_usb+'timelapse')
        move_files('./camera/video/', path_to_usb+'video')
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

# video, best = 1080p at 30 fps
# https://raspberrypi.stackexchange.com/questions/32397/how-to-increase-the-camera-exposure-time
# https://picamera.readthedocs.io/en/release-1.13/api_camera.html#piframeraterange

# TODO ==> add conf elements
