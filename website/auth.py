#routes 
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, Response, send_file, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User, ActivityLog
from .forms import LoginForm, RegisterForm, UserProfileForm, EditForm, AddNewUserForm, SearchForm
from .utils import activity_logs, LoadModel
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
from sqlalchemy import or_
from io import BytesIO
import pandas as pd
from xhtml2pdf import pisa
from werkzeug.utils import secure_filename
import uuid  as uuid
import os
import imghdr
import csv
import io

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
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
    temp = None
    if form.validate_on_submit():
        # Check if user with same email already exists
        temp = [form.firstname.data, form.lastname.data, form.email.data, form.password.data, form.retypepassword.data, form.school.data]
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email already registered exist',  category='error')
            return render_template('register.html', form=form, temp=temp)
        elif form.password.data != form.retypepassword.data:
            flash("Password and Retype Password didn't match try again")
            return render_template('register.html', form=form, temp=temp)
        else:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, school=form.school.data, password=hashed_password, usertype='user', model=LoadModel())
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            activity_logs('New User Registered')
            flash('Account created!', category='success')
            return redirect(url_for('views.dashboard'))
    return render_template('register.html', form=form, temp=temp)

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get_or_404(current_user.id)
    form = EditForm()
    existing_info = {
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
        'school': user.school,
        'profile': user.imagepath
    }
    if request.method == 'POST' and request.form.get('submit'):
        if request.form['firstname'] == '':
            user.firstname = existing_info['firstname']
        if request.form['lastname'] == '':
            user.lastname = existing_info['lastname']
        if request.form['email'] == '':
            user.email = existing_info['email']
        if request.form['school'] == '':
            user.school = existing_info['school']
        if request.files['profile'] == '':
            user.imagepath = existing_info['profile']

        if request.form['firstname']:
            user.firstname = request.form['firstname']
        if request.form['lastname']:
            user.lastname = request.form['lastname']
        if request.form['school']:
            user.school = request.form['school']

        if request.files['profile']:
            if imghdr.what(request.files['profile']) not in ['jpeg', 'jpg', 'png']:
                flash('Invalid file format. Only JPEG, JPG, and PNG files are allowed.', category='error')
                return redirect(url_for('auth.profile'))
            
            old_image_path = None
            if existing_info['profile']:
                old_image_path = os.path.join("website", "static", "profiles", existing_info['profile'])
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)

            profile = secure_filename(request.files['profile'].filename)
            #set the uuid
            profile_filename = str(uuid.uuid1()) + "_" + profile
            saveImage = request.files['profile']
            user.imagepath = profile_filename
            saveImage.save(os.path.join("website", "static", "profiles", profile_filename))

        try:
            db.session.commit()
            activity_logs('Edit user profile')
            flash('Successfully Updated', category='success')
            return redirect(url_for('auth.profile'))
        except:
            flash('Failed to update', category='danger')
            activity_logs('Failed to edit user profile')
            return redirect(url_for('auth.profile'))

    activity_logs("Update Profile")
    return render_template('profile.html', form=form, existing_info=existing_info, current_user=current_user)



@auth.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    if current_user.usertype == 'user' or current_user.usertype == 'professor':
        flash('You dont have permission to access this page', category='error')
        activity_logs("User tried to access accounts function")
        return redirect(url_for('views.dashboard'))
    
    
    accs = User.query.all()
    searchform = SearchForm()
    addform = AddNewUserForm()
    editform = EditForm()
    if addform.validate_on_submit():
        existing_email = User.query.filter_by(email=addform.email.data).first()
        if existing_email:
            flash('Email already registered exist',  category='error')
            return redirect(url_for('auth.accounts'))
        else:
            new_user = User(
                email=addform.email.data,
                password=generate_password_hash(addform.password.data),
                firstname=addform.firstname.data,
                lastname=addform.lastname.data,
                usertype=addform.usertype.data,
                school=addform.school.data,
                model = LoadModel()
            )
            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            activity_logs('Added New User')
            flash('New user added successfully!', category='success')
            return redirect(url_for('auth.accounts'))
    return render_template('accounts.html', accounts=accs, addform=addform, searchform=searchform, editform=editform)

@auth.route('/addaccounts', methods=['GET', 'POST'])
@login_required
def addaccounts():
    
    if current_user.usertype == 'user' or current_user.usertype == 'professor':
        flash('You dont have permission to access this page', category='error')
        activity_logs("User tried to access add accounts function")
        return redirect(url_for('views.dashboard'))
    
    addform = AddNewUserForm()
    if addform.validate_on_submit():
        existing_email = User.query.filter_by(email=addform.email.data).first()
    if existing_email:
        flash('Email already registered exist',  category='error')
        return redirect(url_for('auth.accounts'))
    else:
        new_user = User(
            email=addform.email.data,
            password=generate_password_hash(addform.password.data),
            firstname=addform.firstname.data,
            lastname=addform.lastname.data,
            school=addform.school.data,
            model = LoadModel(),
            usertype=addform.usertype.data
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        activity_logs('Added New User')
        flash('New user added successfully!', category='success')
        return redirect(url_for('auth.accounts'))
    
@auth.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    if current_user.usertype == 'professor' or current_user.usertype == 'student':
       activity_logs('User tried to access the account edit function')
       flash("You dont have permision to access this page")
       return redirect(url_for('views.dashboard'))

    user = User.query.get_or_404(user_id)
    form = EditForm()
    existing_info = {
        'firstname' : user.firstname,
        'lastname' : user.lastname,
        'email' : user.email,
        'school' : user.school,
        'password': user.password,
        'usertype': user.usertype
    }

    if request.method == 'POST' and request.form.get('submit'):

        if request.form['firstname'] == '':
            user.firstname = existing_info['firstname']
        if request.form['lastname'] =='':
            user.lastname = existing_info['lastname']
        if request.form['email'] == '':
            user.email = existing_info['email']
        if request.form['school'] =='':
            user.school = existing_info['school']
        if request.form['password'] =='':
            user.password = existing_info['password']
        if request.form['usertype'] != existing_info['usertype']:
            user.usertype = request.form['usertype']

        if request.form['firstname']:
            user.firstname = request.form['firstname']
        if request.form['lastname']:
            user.lastname = request.form['lastname']
        if request.form['school']:
            user.school = request.form['school']
        if request.form['password']:
            user.password = generate_password_hash(request.form['password'])
        if request.form['email'] != '':
            if User.query.filter_by(email=request.form['email']).first():
                flash('Email already exists', category='danger')
                return redirect(url_for('auth.account'))
            user.email = request.form['email']
        try: 
            db.session.commit()
            activity_logs('Edit user profile')
            flash('Successfully Updated', category='success')
            return redirect(url_for('auth.accounts'))
        except:
            flash('Failed to update', category='danger')
            activity_logs('Failed to edit user profile')
            return redirect(url_for('auth.edit' , user_id = user.id))
    activity_logs('Edit User Account')
    return redirect(url_for('auth.accounts'))

@auth.route('/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete(user_id):
    if current_user.usertype == 'user' or current_user.usertype == 'professor':
        flash('You dont have permission to access this page', category='error')
        activity_logs("User tried to access the delete account function")
        return redirect(url_for('views.student'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found', category='error')
        activity_logs('Deleting Non-existing user')
        return redirect(url_for('auth.accounts'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User deleted', category='success')
    activity_logs('Deleted a user')
    return redirect(url_for('auth.accounts'))

@auth.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if current_user.usertype == 'user' or current_user.usertype == 'professor':
        flash('You dont have permission to access this page', category='error')
        activity_logs("User tried to access the delete account function")
        return redirect(url_for('views.dashboard'))
    
    form = SearchForm()
    addform = AddNewUserForm()
    editform = EditForm()
    if request.method == 'POST' and request.form.get('submit'):
        query_string = form.search.data
        print(query_string)
        results = User.query.filter(or_(User.firstname.ilike(f'%{query_string}%'),
                                      User.lastname.ilike(f'%{query_string}%'),
                                      User.usertype.ilike(f'%{query_string}%'),
                                      User.school.ilike(f'%{query_string}%'),
                                      User.id.ilike(f'%{query_string}%'),
                                      User.email.ilike(f'%{query_string}%'))).all()
        print(results)
        if results is None:
            flash('The User doesnt exists', category='warning')
            activity_logs('failed to search user')
            return redirect('auth.accounts')
        else: 
            activity_logs('Search for a user')
            
            return render_template('search.html', results=results, form=form, addform=addform, editform=editform)
        
    return redirect(url_for('auth.accounts'))
    
@auth.route('/logs')
def logs():
    if current_user.usertype == 'user' or current_user.usertype == 'professor':
        flash('You dont have permission to access this page', category='error')
        activity_logs("User tried to access the logs function")
        return redirect(url_for('views.dashboard'))
    
    today = date.today()
    #logs = ActivityLog.query.all()
    logs = ActivityLog.query.filter(ActivityLog.logtime >= datetime.combine(today, datetime.min.time())).all()
    return render_template('logs.html', log=logs)

# this route will export all the logs
@auth.route('/exalllogs')
def exalllogs():
    if current_user.usertype == 'user' or current_user.usertype == 'professor':
        flash('You dont have permission to access this page', category='error')
        activity_logs("User tried to access the exalllogs function")
        return redirect(url_for('views.dashboard'))
    
    today = date.today()
    logs = ActivityLog.query.all()
    df = pd.DataFrame([(log.user_id, log.name, log.logtime, log.activity) for log in logs],
                      columns=['User ID', 'Fullname', 'Time Log', 'Activity'])
    buffer = BytesIO()
    writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='All Logs')
    writer.close()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'All Logs {today}.xlsx')

# this route will export todays logs
@auth.route('/extodaylog')
def extodaylog():
    if current_user.usertype == 'user' or current_user.usertype == 'professor':
        flash('You dont have permission to access this page', category='error')
        activity_logs("User tried to access the extodaylog function")
        return redirect(url_for('views.dashboard'))
    
    today = date.today()
    logs = ActivityLog.query.filter(ActivityLog.logtime >= today).all()
    df = pd.DataFrame([(log.user_id, log.name, log.logtime, log.activity) for log in logs],
                      columns=['User ID', 'Fullname', 'Time Log', 'Activity'])
    buffer = BytesIO()
    writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Logs Today')
    writer.close()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'Logs Today {today}.xlsx')

@auth.route('/CustomDownload')
def CustomDownload():
    if current_user.usertype == 'user' or current_user.usertype == 'professor':
        flash('You dont have permission to access this page', category='error')
        activity_logs("User tried to access the CustomDownload function")
        return redirect(url_for('views.dashboard'))

    start_date = request.args.get('startdate')
    end_date = request.args.get('enddate')
    
    # format the input strings to datetime objects
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

    # get the logs within the date range
    logs = ActivityLog.query.filter(ActivityLog.logtime >= start_datetime, ActivityLog.logtime <= end_datetime).all()

    # create the csv file
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'User ID', 'Name', 'Log Time', 'Activity'])
    for log in logs:
        writer.writerow([log.id, log.user_id, log.name, log.logtime.strftime('%Y-%m-%d %H:%M:%S'), log.activity])

    # output the file
    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-disposition": "attachment; filename=logs.csv"}
    )

    return response

@auth.route('/images/<filename>')
@login_required
def images(filename):
    return  send_from_directory("images", filename)

#error page handler | page not found
@auth.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#error page handler | Internal server error
@auth.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

@auth.route('/logout')
@login_required
def logout():
    #activity_logs('User Logout')
    session.clear()
    current_user = None
    logout_user()
    return redirect(url_for('auth.home'))

# @auth.route('/edit/<int:user_id>', methods=['GET', 'POST'])
# @login_required
# def edit(user_id):
#     if current_user.usertype == 'user':
#         flash('You dont have permission to access this page', category='error')
#         activity_logs("Try to access webpages not for users")
#         return redirect(url_for('views.student'))
    
#     user = User.query.get_or_404(user_id)
#     form = EditForm()
#     existing_info = {
#         'firstname' : user.firstname,
#         'lastname' : user.lastname,
#         'email' : user.email,
#         'password' : user.password,
#         'usertype' : user.usertype
#     }
#     if request.method == 'POST' and request.form.get('submit'):

#         if request.form['firstname'] != existing_info['firstname']:
#             user.firstname = request.form['firstname']
#         if request.form['lastname'] != existing_info['lastname']:
#             user.lastname = request.form['lastname']
#         if request.form['password'] != existing_info['password']:
#             user.password = generate_password_hash(request.form['password'])
#         if request.form['usertype'] != existing_info['usertype']:
#             user.usertype = request.form['usertype']
#         if request.form['email'] != existing_info['email']:
#             # Check if the new email already exists in the database
#             if User.query.filter_by(email=request.form['email']).first():
#                 flash('Email already exists', category='danger')
#                 return redirect(url_for('auth.edit', user_id=user.id))
#             user.email = request.form['email']

#         if request.form['password'] != request.form['retype']:
#             flash("The password and retype password doesnt match")
#             return redirect(url_for('auth.edit', user_id=user_id))

#         try: 
#             db.session.commit()
#             activity_logs('Edit user profile')
#             flash('Successfully Updated', category='success')
#             return redirect(url_for('auth.accounts'))
#         except:
#             flash('Failed to update', category='danger')
#             activity_logs('Failed to edit user profile')
#             return redirect(url_for('auth.edit' , user_id = user.id))
    
#     return render_template('edit.html', form=form,  existing_info=existing_info)

# @auth.route('/pdfalllogs')
# def pdfalllogs():
#     if current_user.usertype == 'user':
#         flash('You dont have permission to access this page', category='error')
#         activity_logs("The user tried to export the live logs")
#         return redirect(url_for('views.student'))
    
#     logs = ActivityLog.query.all()
#     return render_template('logs_pdf.html', logs=logs)
    

# @auth.route('/pdftodaylogs')
# def pdftodaylogs():
#     if current_user.usertype == 'user':
#         flash('You dont have permission to access this page', category='error')
#         activity_logs("The user tried to export the live logs")
#         return redirect(url_for('views.student'))
    
#     today = date.today()
#     logs = ActivityLog.query.filter(ActivityLog.logtime >= datetime.combine(today, datetime.min.time())).all()
#     return render_template('logs_pdf.html', logs=logs)

# @auth.route('/profile', methods=['GET', 'POST'])
# @login_required
# def profile():
#     user =  User.query.get_or_404(current_user.id)
#     form = UserProfileForm()
#     existing_info = {
#         'firstname' : user.firstname,
#         'lastname' : user.lastname,
#         'email' : user.email,
#         'school' : user.school
#     }
#     if request.method == 'POST' and request.form.get('submit'):
#         if request.form['firstname'] != current_user.firstname:
#             user.firstname = request.form['firstname']
#         if request.form['lastname'] != current_user.lastname:
#                 user.lastname = request.form['lastname']
#         if request.form['email'] != current_user.email:
#             # Check if the new email already exists in the database
#             if User.query.filter_by(email=request.form['email']).first():
#                 flash('Email already exists', category='danger')
#                 return redirect(url_for('auth.profile'))
#             user.email = request.form['email']
#         if request.form['school'] != current_user.school:
#             user.school = request.form['school']
#         try:
#             db.session.commit()
#             flash('Profile Successfully Updated', category='success')
#             activity_logs("User Profile Updated")
#             return redirect(url_for('auth.profile'))
#         except:
#             flash('Profile Failed to Updated', category='danger')
#             activity_logs("User profile failed to updated")
#             return redirect(url_for('auth.profile'))
#     return render_template('profile.html', form=form, existing_info=existing_info, current_user=current_user)