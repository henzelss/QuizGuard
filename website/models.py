from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from werkzeug.security import generate_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    usertype = db.Column(db.String(10))


class QuizBank():
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiztitle = db.Column(db.String(150))
    category = db.Column(db.String(25))

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255))
    logtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    activity = db.Column(db.String(255))
    user = db.relationship('User', backref=db.backref('activity_logs', lazy=True))

