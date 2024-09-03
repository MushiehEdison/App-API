from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = 'c79f0253bccc2592689a322cea09095d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4','avi', 'mov'}
app.config['MAX_CONTENT_LENGTH'] = 20*1024*1024

login_manager.login_view = 'login'
db = SQLAlchemy(app)
from FlaskApp.routes import User, TweetPost, MediaPost