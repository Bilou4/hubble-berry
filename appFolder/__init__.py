from flask import Flask

from appFolder.config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# login_manager = LoginManager()
# login_manager.init_app(app)

from appFolder import routes