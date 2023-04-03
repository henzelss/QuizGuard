from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, SelectField, DateTimeField, RadioField
from wtforms.validators import DataRequired, Email, Length 
from wtforms import ValidationError
from .models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter Your Email"})
    #username = StringField('Enter Your Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Your Password"})
    remember = BooleanField('Remember me') 
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()], render_kw={"placeholder": "Enter Firstname "})
    lastname = StringField('Lastname', validators=[DataRequired()], render_kw={"placeholder": "Enter Lastname"})
    #section = StringField('Enter Your section', validators=[DataRequired()], render_kw={"placeholder": "Enter Section"})
    #username = StringField('Enter Your Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Enter Your Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Password"})
    retypepassword = PasswordField('Retype Password', validators=[DataRequired()], render_kw={"placeholder": "Confirm Your Password"})
    submit = SubmitField('Register')

class UserProfileForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()], render_kw={"placeholder": "Enter Firstname "})
    lastname = StringField('Lastname', validators=[DataRequired()], render_kw={"placeholder": "Enter Lastname"})
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Enter Your Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Password"})
    retypepassword = PasswordField('Retype Password', validators=[DataRequired()], render_kw={"placeholder": "Confirm Your Password"})
    submit = SubmitField('Save Changes')

class EditForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()], render_kw={"placeholder": "Enter Firstname "})
    lastname = StringField('Lastname', validators=[DataRequired()], render_kw={"placeholder": "Enter Lastname"})
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Enter Your Email"})
    usertype = SelectField('Select Usertype', choices=[('admin', 'Admin'), ('professor', 'Professor'), ('user', 'User')])
    submit = SubmitField('Save Changes')

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)

        if kwargs.get('obj'):
            user = kwargs['obj']
            self.firstname.data = user.firstname
            self.lastname.data = user.lastname
            self.email.data = user.email
            self.usertype.data = user.usertype

class AddNewUserForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()], render_kw={"placeholder": "Enter Firstname "})
    lastname = StringField('Lastname', validators=[DataRequired()], render_kw={"placeholder": "Enter Lastname"})
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Enter Your Email"})
    usertype = SelectField('Select Usertype', choices=[('admin', 'Admin'), ('professor', 'Professor'), ('user', 'User')])
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Password"})
    submit = SubmitField('Add')
   
class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()], render_kw={"placeholder": "Search User "})
    submit = SubmitField('Search')

class SearchCode(FlaskForm):
    search = StringField('Search', validators=[DataRequired()], render_kw={"placeholder": "Enter your code here "})
    submit = SubmitField('Search') 

class CreateQuiz(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Enter Quiz Title "})
    category = SelectField('Select Category', choices=[('1', 'Matching Type'), ('2', 'Fill in the blanks'), ('3', 'True or False')])
    submit = SubmitField('Add Quiz') 


class MatchingTypeForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Question "})
    choice1 = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 1"})
    choice2 = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 2"})
    choice3 = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 3"})
    choice4 = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 4"})
    answer =  StringField('Answer', validators=[DataRequired()], render_kw={"placeholder": "Enter Answer"})
    submit = SubmitField('Submit')

class MatchingTypeFormEdit(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Question "})
    choice1 = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 1"})
    choice2 = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 2"})
    choice3 = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 3"})
    choice4 = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 4"})
    answer =  StringField('Answer', validators=[DataRequired()], render_kw={"placeholder": "Enter Answer"})
    submit = SubmitField('Submit')

class FillInTheBlanksForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Question "})
    answer =  StringField('Answer', validators=[DataRequired()], render_kw={"placeholder": "Enter Answer"})
    submit = SubmitField('Submit')

class FillInTheBlanksFormEdit(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Question "})
    answer =  StringField('Answer', validators=[DataRequired()], render_kw={"placeholder": "Enter Answer"})
    submit = SubmitField('Submit')

class TrueOrFalseForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Question "})
    answer = RadioField('Select an option', choices=[('0', 'False'), ('1', 'True')])
    submit = SubmitField('Submit')

class TrueOrFalseFormEdit(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Question "})
    answer = RadioField('Select an option', choices=[('0', 'False'), ('1', 'True')])
    submit = SubmitField('Submit')

