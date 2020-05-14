from flask import Flask
from flask import render_template
from config import Config
from forms import LoginForm

PROJECT_NAME = 'Hubble-Berry'

app = Flask(__name__)
app.config.from_object(Config)
# login_manager = LoginManager()
# login_manager.init_app(app)

@app.route('/')
def hello_world():
    user = {'username': 'Bilou'}
    return render_template('index.html', title=PROJECT_NAME, user=user)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)