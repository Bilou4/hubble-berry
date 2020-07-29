from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from appFolder import db
from appFolder import login_manager


class User(UserMixin, db.Model):
    """Class to model a User

    Args:
        UserMixin (UserMixin): This provides default implementations for the methods that Flask-Login expects user objects to have
        db (SQLAlchemy): The Database we want to use

    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # Relationships
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id')) 

    def __repr__(self):
        """To represent a User with a string

        Returns:
            string: return a string representing a user
        """
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        """Set the password of the User

        Args:
            password (string): password set by the User
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the password indicates by the User is the same as in the database

        Args:
            password (string): password set by the User

        Returns:
            boolean: True if the password matched, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def set_default_role(self):
        """Set the default role for a User
        """
        self.role_id = 2

#1=admin, 2=user
# Define the Role data model
class Role(db.Model):
    """Class to model a User's Role

    Args:
        db (SQLAlchemy): The Database we want to use
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)



# The @login_manager.user_loader piece tells Flask-login how to load users given an id
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))