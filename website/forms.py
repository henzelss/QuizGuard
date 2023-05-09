from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, SelectField, DateTimeField, RadioField, IntegerField, TextAreaField, HiddenField, FileField, TimeField, DateField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from wtforms import ValidationError
from .models import User, MultipleChoice, QuizList
from jinja2 import Markup

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter Your Email", 'autocomplete': 'off'})
    #username = StringField('Enter Your Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Your Password", 'autocomplete': 'off'})
    remember = BooleanField('Remember me') 
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()], render_kw={"placeholder": "Enter Firstname ", 'autocomplete': 'off'})
    lastname = StringField('Lastname', validators=[DataRequired()], render_kw={"placeholder": "Enter Lastname", 'autocomplete': 'off'})
    #section = StringField('Enter Your section', validators=[DataRequired()], render_kw={"placeholder": "Enter Section"})
    #username = StringField('Enter Your Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Enter Your Email", 'autocomplete': 'off'})
    school = StringField('School', validators=[DataRequired()], render_kw={"placeholder": "Enter School Name", 'autocomplete': 'off'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Password", 'autocomplete': 'off'})
    retypepassword = PasswordField('Retype Password', validators=[DataRequired()], render_kw={"placeholder": "Confirm Your Password", 'autocomplete': 'off'})
    submit = SubmitField('Register')

class UserProfileForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()], render_kw={"placeholder": "Enter Firstname ", 'autocomplete': 'off'})
    lastname = StringField('Lastname', validators=[DataRequired()], render_kw={"placeholder": "Enter Lastname", 'autocomplete': 'off'})
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Enter Your Email", 'autocomplete': 'off'})
    school = StringField('School', validators=[DataRequired(), Length(max=50)], render_kw={"placeholder": "Enter Your School", 'autocomplete': 'off'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Password", 'autocomplete': 'off'})
    retypepassword = PasswordField('Retype Password', validators=[DataRequired()], render_kw={"placeholder": "Confirm Your Password", 'autocomplete': 'off'})
    profile = FileField('Profile Picture')
    submit = SubmitField('Save Changes')

class EditForm(FlaskForm):
    firstname = StringField('Firstname',  render_kw={"placeholder": "Enter Firstname ", 'autocomplete': 'off'})
    lastname = StringField('Lastname', render_kw={"placeholder": "Enter Lastname", 'autocomplete': 'off'})
    email = StringField('Email',  render_kw={"placeholder": "Enter Your Email", 'autocomplete': 'off'})
    school = StringField('School', render_kw={"placeholder": "Enter School Name", 'autocomplete': 'off'})
    password = PasswordField('Password', render_kw={"placeholder": "Enter New Password", 'autocomplete': 'off'})
    usertype = SelectField('Select Role', choices=[('admin', 'Admin'), ('professor', 'Professor'), ('user', 'User')])
    profile = FileField('Profile Picture')
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
    firstname = StringField('Firstname', validators=[DataRequired()], render_kw={"placeholder": "Enter Firstname ", 'autocomplete': 'off'})
    lastname = StringField('Lastname', validators=[DataRequired()], render_kw={"placeholder": "Enter Lastname", 'autocomplete': 'off'})
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Enter Your Email", 'autocomplete': 'off'})
    school = StringField('School', validators=[DataRequired()], render_kw={"placeholder": "Enter School Name", 'autocomplete': 'off'})
    usertype = SelectField('Select Role', choices=[('admin', 'Admin'), ('professor', 'Professor'), ('user', 'User')])
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Password", 'autocomplete': 'off'})
    submit = SubmitField('Add')
   
class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()], render_kw={"placeholder": "Search User ", 'autocomplete': 'off'})
    submit = SubmitField('Search')

class SearchCode(FlaskForm):
    search = StringField('Search', validators=[DataRequired()], render_kw={"placeholder": "Enter your code here ", 'autocomplete': 'off'})
    submit = SubmitField('Search') 

class CreateQuiz(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Enter Quiz Title ", 'autocomplete': 'off'})
    category = SelectField('Select Category', choices=[('1', 'Multiple Choice'), ('2', 'Fill in the blanks'), ('3', 'True or False')])
    submit = SubmitField('Add Quiz') 


class MultipleChoiceForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Question", 'autocomplete': 'off'})
    choice1 = StringField('Choice 1', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 1", 'autocomplete': 'off'})
    choice2 = StringField('Choice 2', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 2", 'autocomplete': 'off'})
    choice3 = StringField('Choice 3', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 3", 'autocomplete': 'off'})
    choice4 = StringField('Choice 4', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 4", 'autocomplete': 'off'})
    answer =  StringField('Answer', validators=[DataRequired()], render_kw={"placeholder": "Enter Answer", 'autocomplete': 'off'})
    submit = SubmitField('Submit')

class MultipleChoiceFormEdit(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Question", 'autocomplete': 'off'})
    choice1 = StringField('Choice 1', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 1", 'autocomplete': 'off'})
    choice2 = StringField('Choice 2', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 2", 'autocomplete': 'off'})
    choice3 = StringField('Choice 3', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 3", 'autocomplete': 'off'})
    choice4 = StringField('Choice 4', validators=[DataRequired()], render_kw={"placeholder": "Enter Choice 4", 'autocomplete': 'off'})
    answer =  StringField('Answer', validators=[DataRequired()], render_kw={"placeholder": "Enter Answer", 'autocomplete': 'off'})
    submit = SubmitField('Submit')

class FillInTheBlanksForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Question ", 'autocomplete': 'off'})
    keyword1 = StringField('Keyword 1', validators=[DataRequired()], render_kw={"placeholder": "Enter Keyword 1 ", 'autocomplete': 'off'})
    keyword2 = StringField('Keyword 2', validators=[DataRequired()], render_kw={"placeholder": "Enter Keyword 2 ", 'autocomplete': 'off'})
    keyword3 = StringField('Keyword 3', validators=[DataRequired()], render_kw={"placeholder": "Enter Keyword 3 ", 'autocomplete': 'off'})
    answer =  StringField('Answer', validators=[DataRequired()], render_kw={"placeholder": "Enter Answer", 'autocomplete': 'off'})
    
    submit = SubmitField('Submit')

class FillInTheBlanksFormEdit(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Question ", 'autocomplete': 'off'})
    answer =  StringField('Answer', validators=[DataRequired()], render_kw={"placeholder": "Enter Answer", 'autocomplete': 'off'})
    keyword1 = StringField('Keyword 1', validators=[DataRequired()], render_kw={"placeholder": "Enter Keyword 1 ", 'autocomplete': 'off'})
    keyword2 = StringField('Keyword 2', validators=[DataRequired()], render_kw={"placeholder": "Enter Keyword 2 ", 'autocomplete': 'off'})
    keyword3 = StringField('Keyword 3', validators=[DataRequired()], render_kw={"placeholder": "Enter Keyword 3 ", 'autocomplete': 'off'})
    answer =  StringField('Answer', validators=[DataRequired()], render_kw={"placeholder": "Enter Answer", 'autocomplete': 'off'})
    submit = SubmitField('Submit')

class TrueOrFalseForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Question ", 'autocomplete': 'off'})
    answer = RadioField('Select an option', choices=[('0', 'True'), ('1', 'False')])
    submit = SubmitField('Submit')

class TrueOrFalseFormEdit(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Enter Question ",'autocomplete': 'off'})
    answer = RadioField('Select an option', choices=[('0', Markup('<i class="fa-regular fa-circle-check me-1"></i>True')), ('1', Markup('<i class="fa-regular fa-circle-xmark me-1"></i>False'))])
    submit = SubmitField('Submit')

class QuizForm(FlaskForm):
    title = StringField('Quiz Title', validators=[DataRequired()], render_kw={"placeholder": "Enter Quiz Title", 'autocomplete': 'off'})
    #description = StringField('Quiz Description', validators=[DataRequired()], render_kw={"placeholder": "Enter Quiz Description "})
    description = TextAreaField('Description', render_kw={"placeholder": "Enter your text here", 'autocomplete': 'off'} )
    category = SelectField('Select Category', choices=[('1', 'Language'), ('2', 'Social Studies'), ('3', 'Science'), 
                                                       ('4', 'History'), ('5', 'Programming'), ('6', 'Physics'),
                                                       ('7', 'Biology'), ('8', 'Chemistry'), ('9', 'Geography'),
                                                       ('10', 'Career and Technical Education'), ('11', 'Creative Arts'),
                                                       ('12', 'Drama'), ('13', 'Physical Education'),
                                                       ('14', 'Physchology '), ('15', 'Music '), ('16', 'Technology'), ('17', 'Humanities'),
                                                       ('18', 'Economics'), ('19', 'Literature'), ('20', 'Geography'), ('21', 'General Knowledge')
                                                       ])
    
    timelimit = IntegerField('Time Limit (minutes)', validators=[DataRequired(), NumberRange(min=1, max=100)], render_kw={"placeholder": "Enter Time limit"})
    points = IntegerField('Points', validators=[DataRequired(), NumberRange(min=1, max=100)], render_kw={"placeholder": "Enter points per correct answers"})
    startdate = DateField("Start Date", validators=[DataRequired()])
    enddate = DateField("End Date", validators=[DataRequired()])
    starttime = TimeField("Start Time", validators=[DataRequired()])
    endtime = TimeField("End Time", validators=[DataRequired()])
    quiztype = SelectField('Select Quiz Type', choices=[('1', 'Multiple Choice'), ('2', 'Fill in the blanks'), ('3', 'True or False')])
    visibility = RadioField('Visibility', choices=[('1', Markup('<i class="fa-solid fa-earth-asia me-1"></i>public')), ('2', Markup('<i class="fa-solid fa-lock me-1"></i>private'))])
    quizcode = StringField('Quiz Code', validators=[DataRequired()], render_kw={"readonly": True})
    #attempt = IntegerField('Number of Attempts', validators=[NumberRange(min=0, max=10)])
    attempt = IntegerField('Attempt', validators=[DataRequired(), NumberRange(min=1, max=100)], render_kw={"placeholder": "Enter number of attempts"})
    image = FileField("Quiz Image")
    submit = SubmitField('Save')
    


class BulkInsertForm(FlaskForm):
    description = TextAreaField('Description', render_kw={"placeholder": "Enter your text here", 'autocomplete': 'off'} )


# class QuizForm(FlaskForm):
#     title = StringField('Quiz Title', validators=[DataRequired()], render_kw={"placeholder": "Enter Quiz Title", 'autocomplete': 'off'})
#     #description = StringField('Quiz Description', validators=[DataRequired()], render_kw={"placeholder": "Enter Quiz Description "})
#     description = TextAreaField('Description', render_kw={"placeholder": "Enter your text here", 'autocomplete': 'off'} )
#     category = SelectField('Select Category', choices=[('1', 'Language'), ('2', 'Social Studies'), ('3', 'Science'), 
#                                                        ('4', 'History'), ('5', 'Science'), ('6', 'Physics'),
#                                                        ('7', 'Biology'), ('8', 'Chemistry'), ('10', 'Geography'),
#                                                        ('11', 'Career and Technical Education'), ('12', 'Creative Arts'),
#                                                        ('13', 'Creative Arts'), ('14', 'Drama'), ('15', 'Physical Education'),
#                                                        ('16', 'Physchology '), ('16', 'Music '), ('16', 'Music'), ('17', 'Humanities'),
#                                                        ('18', 'Economics'), ('19', 'Literature'), ('20', 'Geography'), ('21', 'General Knowledge')
#                                                        ])
    
#     quiztype = SelectField('Select Quiz Type', choices=[('1', 'Multiple Choice'), ('2', 'Fill in the blanks'), ('3', 'True or Falls')])
#     timelimit = RadioField('Time Limit', choices=[('5', Markup('<i class="fa-regular fa-clock me-1"></i> 5 mins')), ('10', Markup('<i class="fa-regular fa-clock me-1"></i>10 mins')), 
#                                                   ('15', Markup('<i class="fa-regular fa-clock me-1"></i>15 mins')), ('20', Markup('<i class="fa-regular fa-clock me-1"></i>20 mins')), 
#                                                   ('30', Markup('<i class="fa-regular fa-clock me-1"></i>30 mins')), ('60', Markup('<i class="fa-regular fa-clock me-1"></i> 60 mins')), 
#                                                   ('120', Markup('<i class="fa-regular fa-clock me-1"></i>120 mins'))])
    
#     points  = RadioField('Points Per Score', choices=[('1', Markup('<i class="fa-solid fa-medal me-1"></i>1 point')), 
#                                                       ('2', Markup('<i class="fa-solid fa-medal me-1"></i>2 points')), 
#                                                       ('5', Markup('<i class="fa-solid fa-medal me-1"></i>5 points')), 
#                                                       ('10', Markup('<i class="fa-solid fa-medal me-1"></i>10 points')), 
#                                                       ('15', Markup('<i class="fa-solid fa-medal me-1"></i>15 points')), 
#                                                       ('20', Markup('<i class="fa-solid fa-medal me-1"></i>20 points')), 
#                                                       ('30', Markup('<i class="fa-solid fa-medal me-1"></i>30 points')), 
#                                                       ('50', Markup('<i class="fa-solid fa-medal me-1"></i>50 points'))])
#     visibility = RadioField('Visibility', choices=[('1', Markup('<i class="fa-solid fa-earth-asia me-1"></i>public')), ('2', Markup('<i class="fa-solid fa-lock me-1"></i>private'))])
#     quizcode = StringField('Quiz Code', validators=[DataRequired()], render_kw={"readonly": True})
#     #attempt = IntegerField('Number of Attempts', validators=[NumberRange(min=0, max=10)])
#     attempt = RadioField('Number of Attempts', choices=[('100', Markup('<i class="fa-solid fa-pen me-1"></i> Infinite')), ('1', Markup('<i class="fa-solid fa-pen me-1"></i> 1 Attempts')),
#                                                         ('2', Markup('<i class="fa-solid fa-pen me-1"></i> 2 Attempts')), ('3', Markup('<i class="fa-solid fa-pen me-1"></i> 3 Attempts')), 
#                                                         ('5', Markup('<i class="fa-solid fa-pen me-1"></i> 5 Attempts')), ('10', Markup('<i class="fa-solid fa-pen me-1"></i> 10 Attempts'))
#                                                         ])
#     submit = SubmitField('Save')