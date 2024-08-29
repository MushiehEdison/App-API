from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, EmailField,PasswordField, SubmitField, BooleanField, FileField,HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from FlaskApp.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('sign-up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('sign-in')
    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValueError('That username is taken. please choose a different one')
    def validate_email(self, email):
        user=User.query.filter_by(email = email.data).first()
        if user:
            raise ValueError('That email is taken. please choose a different one')
class UpdateAccount(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=4, max=20)])
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=20)])
    email = EmailField('email', validators=[DataRequired(), Email()])
    profile_image = FileField('Upload Profile picture',validators=[FileAllowed(['jpg','jpeg','png','gif','webp'])])
    submit = SubmitField('save')

    def validate_username(self, username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValueError('That username is taken. please choose a different one')
    def validate_email(self, email):
        if email.data != current_user.email:
            user=User.query.filter_by(email = email.data).first()
            if user:
                raise ValueError('That email is taken. please choose a different one')

class UploadPost(FlaskForm):
    tweet = StringField('tweert',validators=[DataRequired(), Length(max=500)])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg','jpeg','png','gif','webp'])])
    video = FileField('Upload Video', validators=[FileAllowed(['mp4','avi','mov'])])
    caption = StringField('tweert', validators=[DataRequired(), Length(max=100)])
    action = HiddenField('Action')
    submit_tweet = SubmitField('Post tweet')
    submit_media = SubmitField('Post Image/Video')