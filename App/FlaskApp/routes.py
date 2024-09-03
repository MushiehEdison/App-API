import os
from PIL import Image
from moviepy.editor import VideoFileClip
from flask import render_template, url_for, flash, redirect, request, session,current_app
from FlaskApp import app, db, bcrypt
from FlaskApp.form import RegistrationForm, LoginForm, UpdateAccount, UploadPost
from FlaskApp.models import User,TweetPost, MediaPost, time_ago
from flask_login import login_user, logout_user, current_user, login_required
import secrets
from werkzeug.utils import secure_filename
from itertools import chain
from datetime import  datetime
from operator import attrgetter

def time_ago(time):
    now = datetime.utcnow()
    diff = now - time

    seconds = diff.total_seconds()
    minutes = int(seconds // 60)
    hours = int(minutes // 60)
    days = int(hours // 24)
    weeks = int(days // 7)

    if seconds < 60:
        return "just now"
    elif minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif days < 7:
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif weeks < 5:
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    else:
        return time.strftime('%B %d, %Y')
@app.route('/')
def home():
    tweets = TweetPost.query.filter_by(username=current_user.username).all()
    mediaa = MediaPost.query.filter_by(username=current_user.username).all()
    Posts = tweets + mediaa
    posts_sorted = sorted(Posts, key=lambda post: post.timestamp, reverse=True)
    for post in Posts:
        post.time_ago = time_ago(post.timestamp)
    combined_posts = sorted(chain(tweets, mediaa), key=attrgetter('timestamp'), reverse=True)
    image_file = url_for('static', filename='image/' + current_user.image_file)
    return render_template('Dashboard.html', image_file=image_file, posts=combined_posts, post =posts_sorted)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect('register')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('login')
    # Render the registration form template
    return render_template('sign-up.html')



@app.route('/login', methods = ['GET', 'POST'])
def login():
    print("Form submitted")
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        print("Form validated")
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print("User found:", user.username)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            print("Login successful")
            return redirect(url_for('account'))
        else:
            print("Login failed: Incorrect username or password")
            flash('Login Unsuccessful. Please try Again', 'danger')
    else:
        print("Form not validated")
    return render_template('sign-in.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('login')

@app.route('/account')
def account():
    tweets = TweetPost.query.filter_by(username=current_user.username).all()
    mediaa = MediaPost.query.filter_by(username=current_user.username).all()
    combined_posts = sorted(chain(tweets, mediaa), key=attrgetter('timestamp'), reverse=True)
    image_file = url_for('static', filename='image/' + current_user.image_file)
    return render_template('Account.html', image_file=image_file , posts=combined_posts)

def save_picture(p_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(p_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(current_app.root_path,'static/image', image_fn)


    output_size = (1000, 1000)
    i = Image.open(p_image)
    i.thumbnail(output_size)
    i.save(image_path)
    print(image_fn)
    return image_fn

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.profile_image.data:
            profile_image = save_picture(form.profile_image.data)
            current_user.image_file = profile_image
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect('profile')

        flash(' Your Account was updated','success')
    elif request.method == 'GET':
        form.name.data=current_user.name
        form.username.data=current_user.username
        form.email.data=current_user.email

    image_file = url_for('static', filename='image/'+ current_user.image_file)
    return render_template('edit.html',image_file=image_file, form=form)

def media(p_media):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(p_media.filename)
    media_fn = random_hex + f_ext
    media_path = os.path.join(current_app.root_path, 'static/post_made', media_fn)

    if f_ext.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        i = Image.open(p_media)
        i.save(media_path)
    elif f_ext.lower() in ['.mp4', '.avi', '.mov', '.wmv']:
        p_media.save(media_path)
        clip = VideoFileClip(media_path)
        clip.write_videofile(media_path)
    else:
        p_media.save(media_path)

    return media_fn, f_ext


@app.route('/post/new', methods=['POST','GET'])
@login_required
def post():
    form = UploadPost()
    if form.validate_on_submit():
        if request.form['tweet']:
            print('valid')
            new_post = TweetPost(username=current_user.username, tweet=form.tweet.data,userID=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            print('tweet posted')
            flash('Your Post has been uploaded', 'success')
            return redirect(url_for('home'))
        else:
            print('valid')
            if form.image.data:
                media_path, media_ext = media(form.image.data)
                media_post= MediaPost(username=current_user.username, mediaPath=media_path, mediaExt=media_ext, caption=form.caption.data, userID=current_user.id)
                db.session.add(media_post)
                db.session.commit()
                print('image was posted')
                flash('Your Post has been uploaded', 'success')
                return redirect(url_for('home'))
            elif form.video.data:
                media_path, media_ext = media(form.video.data)
                media_post = MediaPost(username=current_user.username, mediaPath=media_path, mediaExt=media_ext,
                                       caption=form.caption.data, userID=current_user.id)
                db.session.add(media_post)
                db.session.commit()
                print('video was posted')

    return render_template('CreatePost.html', form=form)

