from FlaskApp import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timezone
from flask import current_app
import pytz
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_file= db.Column(db.String(120),nullable=False , default='thorfinn.jpg')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        self.name = name
        self.username = username
        self.email = email
        return f"User('{self.username}', '{self.email}', '{self.name}')"
class TweetPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    tweet = db.Column(db.String(5000), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    userID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.username}', '{self.tweet}', '{self.timestamp}')"
class MediaPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    mediaPath = db.Column(db.String(5000), nullable=True)
    mediaExt = db.Column(db.String(10), nullable=True)
    caption = db.Column(db.String(5000), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    userID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    def __repr__(self):
        return f" Post('{self.username}', '{self.caption}','{self.mediaPath}', '{self.timestamp}','{self.mediaExt}') "

def time_ago(time):
    now = datetime.now(pytz.utc)
    time = time.astimezone(pytz.utc)
    diff = now - time

    seconds = diff.total_seconds()
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif minutes < 60:
        return f"{int(minutes)} minutes ago"
    elif hours < 24:
        return f"{int(hours)} hours ago"
    else:
        return f"{int(days)} days ago"




