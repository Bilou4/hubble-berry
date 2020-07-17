from flask import Flask
from flask import request

from appFolder.config import Config, init_logger

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # redirige l'user vers la page 'login' si non connecté
babel = Babel(app)
logger = init_logger(__name__, True)
from appFolder import routes, models

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])