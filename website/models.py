from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from werkzeug.security import generate_password_hash
import pytz

tz = pytz.timezone('Asia/Manila')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    school = db.Column(db.String(150))
    imagepath = db.Column(db.String(150))
    usertype = db.Column(db.String(10))

class QuizList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(10), nullable=False)
    quiztype = db.Column(db.String(10), nullable=False)
    startdate = db.Column(db.Date, nullable=True)   
    enddate = db.Column(db.Date, nullable=True)
    timelimit = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.Integer, nullable=False)
    attempt = db.Column(db.Integer, nullable=False)

class MultipleChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_code = db.Column(db.String(20), db.ForeignKey('quiz_list.code'), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    choice1 = db.Column(db.String(255), nullable=False)
    choice2 = db.Column(db.String(255), nullable=False)
    choice3 = db.Column(db.String(255), nullable=False)
    choice4 = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)

class FillInTheBlanks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_code = db.Column(db.String(20), db.ForeignKey('quiz_list.code'), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)

class TrueOrFalse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_code = db.Column(db.String(20), db.ForeignKey('quiz_list.code'), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Boolean, nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz_list.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    

# class Violations(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     detected = db.Column(db.String(50))
#     multiple_people = db.Column(db.String(50))
#     phone_detected = db.Column(db.String(50))
#     focus = db.Column(db.String(50))
#     switch_tabs = db.Column(db.String(50))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
#     quiz_code = db.Column(db.String(20), db.ForeignKey('quiz_list.code'), nullable=False)


# class Violations(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     laptop = db.Column(db.String(50))
#     phone = db.Column(db.String(50))
#     head_pose = db.Column(db.String(50))
#     switch_tabs = db.Column(db.String(50))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
#     quiz_code = db.Column(db.String(20), db.ForeignKey('quiz_list.code'), nullable=False)

class Violations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    laptop = db.Column(db.String(50))
    laptop_image = db.Column(db.String(50))
    laptop_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(tz))
    phone = db.Column(db.String(50))
    phone_image = db.Column(db.String(50))
    phone_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(tz))
    head_pose = db.Column(db.String(50))
    head_pose_image = db.Column(db.String(50))
    head_pose_image_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(tz))
    switch_tabs = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    quiz_code = db.Column(db.String(20), db.ForeignKey('quiz_list.code'), nullable=False)



    
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_code = db.Column(db.String(20), db.ForeignKey('quiz_list.code'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    toast_message = db.Column(db.String(255))
    status = db.Column(db.String(255))

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255))
    logtime = db.Column(db.DateTime, nullable=False, default=datetime.now(tz))
    activity = db.Column(db.String(255))
    user = db.relationship('User', backref=db.backref('activity_logs', lazy=True))

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz_list.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_taken = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Achievements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image_path = db.Column(db.String(255))

