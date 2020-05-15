from flask import Flask, render_template, flash, redirect,\
     url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import LoginForm

PROJECT_NAME = 'Hubble-Berry'

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# login_manager = LoginManager()
# login_manager.init_app(app)

from app import routes, models

@app.route('/')
@app.route('/index')
def index():
    user = {'username': ''}
    return render_template('index.html', title=PROJECT_NAME, user=user)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)