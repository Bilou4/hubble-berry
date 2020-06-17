from appFolder import app, db
from appFolder.models import User
from appFolder.forms import LoginForm, RegistrationForm

from flask import render_template, flash, redirect,\
     url_for, request, Response
from flask_login import current_user, login_user, logout_user,\
    login_required
from werkzeug.urls import url_parse

from datetime import datetime
from appFolder.camera import Camera

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
        return redirect(url_for('direct'))
    return render_template('index.html', title=PROJECT_NAME + '- Index')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('direct'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '': # empecher l'utilisateur de rediriger vers un site malicieux
            next_page = url_for('direct')
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
        #user.set_default_role()
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title=PROJECT_NAME + '- Register', form=form)


@app.route('/direct', methods=['GET','POST'])
@login_required
def direct():
    return render_template('direct.html', role=current_user.roles[0].name, title=PROJECT_NAME + '- Direct')


@app.route('/take_a_photo', methods=['POST'])
@login_required
def take_a_photo():
    path = request.form['path']
    exposure_photo = request.form['exposure_photo']
    print(path + exposure_photo)
    return {"text":"photo prise!","name": datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}


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
    timelapse_name = timelapse_name.split('Timelapse en cours')[1]
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
    video_name = video_name.split('Vidéo en cours')[1]
    return {"text":"Vidéo terminée","name": video_name}


# commencer le timelapse (ou photo avec ouverture) ==> temps d'attente
# Admin vs non admin => error register
# in <p id="message"> add a filename span to avoid split('Timelapse en cours') 
