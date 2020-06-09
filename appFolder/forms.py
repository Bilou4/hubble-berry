from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange

from appFolder.models import User

class LoginForm(FlaskForm):
    username = StringField('Who are you?', validators=[DataRequired()])
    password = PasswordField('What is your password?', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Go!')




class RegistrationForm(FlaskForm):
    username = StringField('How may I call you?', validators=[DataRequired()], render_kw={"placeholder": "USERNAME"})
    email = StringField('How may I reach you?', validators=[DataRequired(), Email()], render_kw={"placeholder": "username@example.com"})
    password = PasswordField('Choose a strong password', validators=[DataRequired()], render_kw={"placeholder": "****"})
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "****"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is already taken.')


