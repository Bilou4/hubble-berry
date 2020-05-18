from appFolder import app
from appFolder.models import User
from appFolder.forms import LoginForm

from flask import render_template, flash, redirect,\
     url_for, request
from flask_login import current_user, login_user, logout_user,\
    login_required
from werkzeug.urls import url_parse
PROJECT_NAME = 'Hubble-Berry'



@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title=PROJECT_NAME)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '': # empecher l'utilisateur de rediriger vers un site malicieux
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)