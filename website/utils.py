# from werkzeug.security import generate_password_hash
from . import db
from .models import ActivityLog, Violations
from datetime import datetime
from flask_login import current_user
import random
import string

# Activity logs
def activity_logs(action): 
    fullname = current_user.firstname + " " + current_user.lastname
    new_log_entry = ActivityLog(user_id=current_user.id, name=fullname, activity=action)
    db.session.add(new_log_entry)
    db.session.commit()
# Code Generator
def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for i in range(length)))

def check_category(category):
   if category == '1':
       return "Language"
   elif category == '2':
       return "Social Studies"
   elif category == '3':
       return "Science"
   elif category == '4':
       return "History"
   elif category == '5':
       return "Programming"
   elif category == '6':
       return "Physics"
   elif category == '7':
       return "Biology"
   elif category == '8':
       return "Chemistry"
   elif category == '9':
       return "Geography"
   elif category == '10':
       return "Career and Technical Education"
   elif category == '11':
       return "Creative Arts"
   elif category == '12':
       return "Drama"
   elif category == '13':
       return "Physical Education"
   elif category == '14':
       return "Physchology"
   elif category == '15':
       return "Music"
   elif category == '16':
       return "Technology"
   elif category == '17':
       return "Humanities"
   elif category == '18':
       return "Economics"
   elif category == '19':
       return "Literature"
   elif category == '20': 
       return "Geography"
   elif category == '21':
       return "General Knowledge"
   
def LoadModel():
    random_number = random.randint(1, 4)
    return random_number