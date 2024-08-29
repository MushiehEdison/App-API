import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session,current_app
from FlaskApp import app, db, bcrypt
from FlaskApp.form import RegistrationForm, LoginForm, UpdateAccount
from FlaskApp.models import User
from flask_login import login_user, logout_user, current_user, login_required
import secrets
@app.route('/')
def home():
    image_file = url_for('static', filename='image/'+ current_user.image_file)
    return render_template('Dashboard.html', image_file=image_file)

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
            return redirect('login')
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
    image_file = url_for('static', filename='image/' + current_user.image_file)
    return render_template('Account.html', image_file=image_file)

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

