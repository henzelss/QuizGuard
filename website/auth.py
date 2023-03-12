#routes 
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User, ActivityLog
from .forms import LoginForm, RegisterForm, UserProfileForm
from .utils import activity_logs
auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/home', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        firstname = current_user.firstname
        lastname = current_user.lastname
        fullname = current_user.firstname + " " + current_user.lastname
        return redirect(url_for('views.dashboard'))
    
    form = LoginForm() # check the user info
    temp = None
    if form.validate_on_submit():
        temp = [form.email.data, form.password.data]
        user = User.query.filter_by(email=form.email.data).first()

        if user: #check if the email exist
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data) # remember me function
                activity_logs('Login')
                return redirect(url_for('views.dashboard'))
            else :
                flash('Incorrect password, try again', category='error')
        else: 
            flash('Email does not exist.', category='error')
    return render_template('home.html', form=form, temp=temp)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    dict = {}
    if form.validate_on_submit():
        # Check if user with same email already exists
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email already registered exist',  category='error')
            return redirect(url_for('auth.register'))
        elif form.password.data != form.retypepassword.data:
            flash("Password and Retype Password didn't match try again")
            return redirect(url_for('auth.register'))
        else:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password, usertype='admin')
            db.session.add(new_user)
            db.session.commit()
            activity_logs('New User Registered')
            flash('Account created!', category='success')
            return redirect(url_for('views.dashboard'))
    return render_template('register.html', form=form)


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UserProfileForm()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        db.session.commit()
        activity_logs('Update Profile')
        flash('Your profile has been updated!', category='success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        print('Nothing!')

    print('Nothing Happening!')
    return render_template('profile.html', form=form)

@auth.route('/accounts')


@auth.route('/logs')
def logs():
    logs = ActivityLog.query.all()
    return render_template('logs.html', log=logs)


@auth.route('/logout')
@login_required
def logout():
    #activity_logs('User Logout')
    logout_user()
    return redirect(url_for('auth.home'))

