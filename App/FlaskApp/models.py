from FlaskApp import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timezone
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
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
class Post( ):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_video_file = db.Column(db.String(20), nullable=False)
    tweet = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        self.username = current_user.username
        self.caption = caption
        self.tweet = tweet
        self.image_video_file= image_video_file
        self.timestamp=timestamp
        return f"User('{self.username}', '{self.caption}', '{self.tweet}', '{self.image_video_file}','{self.timestamp}')"