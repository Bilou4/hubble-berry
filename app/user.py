from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin


class User(UserMixin):
    def __init__(self):
        super().__init__()
        self.username = 'user'
        self.password_hash = generate_password_hash('password')
        self.id = 1

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Admin(User):
    def __init__(self):
        super().__init__()
        self.username = 'admin'
        self.password_hash = generate_password_hash('admin')
        self.id = 2

@login.user_loader
def load_user(id):
    return User.get(id)