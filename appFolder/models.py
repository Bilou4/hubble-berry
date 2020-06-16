from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from appFolder import db
from appFolder import login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
                backref=db.backref('blabla', lazy=True))

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_default_role(self):
        self.roles.append(UserRoles(user_id=self.id, role_id=2)) #1=admin, 2=user

# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles data model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))



# The @login_manager.user_loader piece tells Flask-login how to load users given an id
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))