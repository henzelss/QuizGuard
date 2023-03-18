#routes 
from flask import Blueprint, render_template, url_for, flash, redirect, send_from_directory, jsonify, request, Response
from flask_login import login_required, current_user
from .models import User
from .import db

views = Blueprint('views', __name__)




@views.route('/dashboard')
@login_required
def dashboard():
    user =  User.query.get_or_404(current_user.id)

    print('Login Successfully')
    print(f'User type: {current_user.usertype}')
    if current_user.usertype == 'user':
        return render_template('student.html')
    elif current_user.usertype == 'admin':
        return render_template('admin.html')
    elif current_user.usertype == 'professor':
        return render_template('professor.html')

    # If the user's usertype is not recognized, redirect to a custom error page
    return render_template('error.html', message='Unknown user type')


@views.route('/SearchQuiz')
def SearchQuiz():
    return render_template('quizcode.html')


@views.route('createquiz')
def createquiz():
    return render_template('quiz.html')



@views.route('/images/<filename>')
def images(filename):
    return  send_from_directory("images", filename)





@views.route('/quizbank')
def quizbank():
    return render_template('quizbank.html')

#error page handler | page not found
@views.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#error page handler | Internal server error
@views.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

