# from werkzeug.security import generate_password_hash
from . import db
from .models import ActivityLog
from datetime import datetime
from flask_login import current_user


# Activity logs
def activity_logs( action): 
    fullname = current_user.firstname + " " + current_user.lastname

    new_log_entry = ActivityLog(user_id=current_user.id, name=fullname, activity=action)
    db.session.add(new_log_entry)
    db.session.commit()



# # from .utils import create_defualt_admin,  create_defualt_professor
# # create_defualt_admin()
# # create_defualt_professor()


# def create_defualt_admin():
#     email = 'admin@gmail.com'
#     password = 'admin123'
#     existing_admin = User.query.filter_by(email=email, usertype='admin').first()
#     if existing_admin is None:
#         hashed_password = generate_password_hash(password, method='sha256')
#         new_admin = User(firstname='admin', lastname='admin', section='admin', email=email, password=hashed_password, usertype='admin')
#         db.session.add(new_admin)
#         db.session.commit()
#         print('Default admin account created.')
#     else:
#         print('Default admin account already exists.')

# def create_defualt_professor():
#     email = 'professor@gmail.com'
#     password = 'prof123'
#     existing_admin = User.query.filter_by(email=email, usertype='admin').first()
#     if existing_admin is None:
#         hashed_password = generate_password_hash(password, method='sha256')
#         new_admin = User(firstname='Henzel', lastname='Lagahit', section='professor', email=email, password=hashed_password, usertype='admin')
#         db.session.add(new_admin)
#         db.session.commit()
#         print('Default admin account created.')
#     else:
#         print('Default admin account already exists.')
