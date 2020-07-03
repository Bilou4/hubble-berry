from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange

from flask_babel import lazy_gettext as _l

from appFolder.models import User

class LoginForm(FlaskForm):
    username = StringField(_l('Who are you?'), validators=[DataRequired()])
    password = PasswordField(_l('What is your password?'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Go!'))




class RegistrationForm(FlaskForm):
    username = StringField(_l('How may I call you?'), validators=[DataRequired()], render_kw={"placeholder": "USERNAME"})
    email = StringField(_l('How may I reach you?'), validators=[DataRequired(), Email()], render_kw={"placeholder": "username@example.com"})
    password = PasswordField(_l('Choose a strong password'), validators=[DataRequired()], render_kw={"placeholder": "****"})
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "****"})
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('This username is already taken.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('This email address is already taken.'))


