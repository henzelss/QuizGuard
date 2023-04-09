from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, SelectField, DateTimeField, RadioField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from wtforms import ValidationError
from .models import User
from jinja2 import Markup



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter Your Email", 'autocomplete': 'off'})
    #username = StringField('Enter Your Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Your Password", 'autocomplete': 'off'})
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
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter New Password"})
    retype = PasswordField('Retype Password', validators=[DataRequired()], render_kw={"placeholder": "Confirm Your Password"})
    usertype = SelectField('Select Role', choices=[('admin', 'Admin'), ('professor', 'Professor'), ('user', 'User')])
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
    usertype = SelectField('Select Role', choices=[('admin', 'Admin'), ('professor', 'Professor'), ('user', 'User')])
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
    category = SelectField('Select Category', choices=[('1', 'Multiple Choice'), ('2', 'Fill in the blanks'), ('3', 'True or False')])
    submit = SubmitField('Add Quiz') 


class MultipleChoiceForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Question "})
    choice1 = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 1"})
    choice2 = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 2"})
    choice3 = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 3"})
    choice4 = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 4"})
    answer =  StringField('Answer', validators=[DataRequired()], render_kw={"placeholder": "Enter Answer"})
    submit = SubmitField('Submit')

class MultipleChoiceFormEdit(FlaskForm):
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

class QuizForm(FlaskForm):
    title = StringField('Quiz Title', validators=[DataRequired()], render_kw={"placeholder": "Enter Quiz Title "})
    #description = StringField('Quiz Description', validators=[DataRequired()], render_kw={"placeholder": "Enter Quiz Description "})
    description = TextAreaField('Description', render_kw={"placeholder": "Enter your text here"} )
    category = SelectField('Select Category', choices=[('1', 'Language'), ('2', 'Social Studies'), ('3', 'Science'), 
                                                       ('4', 'History'), ('5', 'Science'), ('6', 'Physics'),
                                                       ('7', 'Biology'), ('8', 'Chemistry'), ('10', 'Geography'),
                                                       ('11', 'Career and Technical Education'), ('12', 'Creative Arts') 
                                                       ])
    
    quiztype = SelectField('Select Quiz Type', choices=[('1', 'Multiple Choice'), ('2', 'Fill in the blanks'), ('3', 'True or Falls')])
    timelimit = RadioField('Time Limit', choices=[('5', Markup('<i class="fa-regular fa-clock me-1"></i> 5 mins')), ('10', Markup('<i class="fa-regular fa-clock me-1"></i>10 mins')), 
                                                  ('15', Markup('<i class="fa-regular fa-clock me-1"></i>15 mins')), ('20', Markup('<i class="fa-regular fa-clock me-1"></i>20 mins')), 
                                                  ('30', Markup('<i class="fa-regular fa-clock me-1"></i>30 mins')), ('60', Markup('<i class="fa-regular fa-clock me-1"></i> 60 mins')), 
                                                  ('120', Markup('<i class="fa-regular fa-clock me-1"></i>120 mins'))])
    
    points  = RadioField('Points Per Score', choices=[('1', Markup('<i class="fa-solid fa-medal me-1"></i>1 point')), 
                                                      ('2', Markup('<i class="fa-solid fa-medal me-1"></i>2 points')), 
                                                      ('5', Markup('<i class="fa-solid fa-medal me-1"></i>5 points')), 
                                                      ('10', Markup('<i class="fa-solid fa-medal me-1"></i>10 points')), 
                                                      ('15', Markup('<i class="fa-solid fa-medal me-1"></i>15 points')), 
                                                      ('20', Markup('<i class="fa-solid fa-medal me-1"></i>20 points')), 
                                                      ('30', Markup('<i class="fa-solid fa-medal me-1"></i>30 points')), 
                                                      ('50', Markup('<i class="fa-solid fa-medal me-1"></i>50 points'))])
    visibility = RadioField('Visibility', choices=[('1', Markup('<i class="fa-solid fa-earth-asia me-1"></i>public')), ('2', Markup('<i class="fa-solid fa-lock me-1"></i>private'))])
    quizcode = StringField('Quiz Code', validators=[DataRequired()], render_kw={"readonly": True})
    #attempt = IntegerField('Number of Attempts', validators=[NumberRange(min=0, max=10)])
    attempt = RadioField('Number of Attempts', choices=[('0', Markup('<i class="fa-solid fa-pen me-1"></i> Infinite')), ('1', Markup('<i class="fa-solid fa-pen me-1"></i> 1 Attempts')),
                                                        ('2', Markup('<i class="fa-solid fa-pen me-1"></i> 2 Attempts')), ('3', Markup('<i class="fa-solid fa-pen me-1"></i> 3 Attempts')), 
                                                        ('5', Markup('<i class="fa-solid fa-pen me-1"></i> 5 Attempts')), ('10', Markup('<i class="fa-solid fa-pen me-1"></i> 10 Attempts'))
                                                        ])
    submit = SubmitField('Save')

    
    