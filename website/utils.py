# from werkzeug.security import generate_password_hash
from . import db
from .models import ActivityLog
from datetime import datetime
from flask_login import current_user
import random
import string

# Activity logs
def activity_logs( action): 
    fullname = current_user.firstname + " " + current_user.lastname
    new_log_entry = ActivityLog(user_id=current_user.id, name=fullname, activity=action)
    db.session.add(new_log_entry)
    db.session.commit()
# Code Generator
def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for i in range(length)))

