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

@app.route('/take_a_photo', methods=['POST'])
@login_required
def take_a_photo():
    path = request.form['path']
    exposure_photo = request.form['exposure_photo']
    print(path + exposure_photo)
    return {"text":"photo en cours!","name": datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}

@app.route('/stop_photo', methods=['POST'])
@login_required
def stop_photo():
    photo_name = request.form['photo_name']
    photo_is_canceled = request.form['cancel']
    # cannot use python boolean type because the request sent a string
    if photo_is_canceled == 'true':
        return {"text":"photo annulée", "name": "-- supprimée --"}
    else:
        with picamera.PiCamera() as camera:
            camera.resolution = (1280,720)
            sleep(2)
            camera.capture('./camera/pictures/'+photo_name,format='png')
        return {"text":"photo prise!","name":photo_name}

@app.route('/take_timelapse', methods=['POST'])
@login_required
def take_timelapse():
    path = request.form['path']
    exposure_photo = request.form['exposure_photo']
    time_between_photos = request.form['time_between_photos']
    number_photos = request.form['number_photos']
    print(path + " " + exposure_photo + " " + time_between_photos + " " +number_photos)
    return {"text":"Timelapse en cours","name": datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}


@app.route('/stop_timelapse', methods=['POST'])
@login_required
def stop_timelapse():
    timelapse_name = request.form['timelapse_name']
    return {"text":"Timelapse terminé","name": timelapse_name}

@app.route('/start_video', methods=['POST'])
@login_required
def start_video():
    path = request.form['path']
    print(path)
    return {"text":"Vidéo en cours","name": datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}

@app.route('/stop_video', methods=['POST'])
@login_required
def stop_video():
    video_name = request.form['video_name']
    return {"text":"Vidéo terminée","name": video_name}


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

# transfert photos sur clé
# camera integration
# 1 page de preview (couper connexions si photo en cours / bientot en cours)
# => ajax appelle preview et délivre 404 
