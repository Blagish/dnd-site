import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm#, HistoryForm, PostForm, CharacterForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


@app.route("/")
@app.route("/home")
def home():
    posts=[]
    image_file_small=''
    if current_user.is_authenticated:
        image_file_small = current_user.avatar(32)
    return render_template('home.html', image_file_small=image_file_small)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/my_profile", methods=['GET', 'POST'])
@login_required
def my_profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Информация обновлена!', 'success')
        return redirect(url_for('my_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('profile.html', title='Account',
                           image_file=current_user.avatar(128), image_file_small=current_user.avatar(32), form=form)


@app.route('/user/<int:user_id>')
@login_required
def user(user_id):
    current_user = User.query.filter_by(username=user_id).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
       {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=current_user, posts=posts)
