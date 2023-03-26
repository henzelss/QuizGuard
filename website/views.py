#routes 
from flask import Blueprint, render_template, url_for, flash, redirect, send_from_directory, jsonify, request, Response
from datetime import datetime, time
from flask_login import login_required, current_user
from .models import User, QuizList, MatchingType, FillInTheBlanks, TrueOrFalse, Violations
from .forms import CreateQuiz, MatchingTypeForm, FillInTheBlanksForm, TrueOrFalseForm
from .utils import generate_random_string, activity_logs
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

@views.route('/error')
@login_required
def error():
    return render_template('error.html')


@views.route('/SearchQuiz')
@login_required
def SearchQuiz():
    return render_template('quizcode.html')




@views.route('/createquiz', methods=['GET', 'POST'])
@login_required
def createquiz():
    form = CreateQuiz()
   
    if request.method == 'POST' and request.form.get('submit'):

        startdate_str = request.form['startdate']
        startdate = datetime.strptime(startdate_str, '%Y-%m-%d').date()

        starttime_str = request.form['starttime']
        starttime = datetime.strptime(starttime_str, '%H:%M').time()
      

        enddate_str = request.form['enddate']
        enddate = datetime.strptime(enddate_str, '%Y-%m-%d').date()

        time_closed_str = request.form['time_closed']
        time_closed = datetime.strptime(time_closed_str, '%H:%M').time()

        new_quiz = QuizList(code=generate_random_string(8), 
                            title=form.title.data, 
                            author_id=current_user.id, 
                            category=form.category.data, 
                            startdate=startdate,
                            starttime=starttime,
                            enddate=enddate,
                            time_closed=time_closed
                            )

        db.session.add(new_quiz)
        db.session.commit()
        activity_logs('Added New Quiz')
        flash('New quiz successfully added!', category='success')
        return redirect(url_for('views.questionaire', quiz_id=current_user.id, category=form.category.data))
        
    return render_template('createquiz.html', form=form)


@views.route('/questionaire/<int:quiz_id>/<string:category>', methods=['GET', 'POST'])
@login_required
def questionaire(quiz_id, category):


    quiz = QuizList.query.get(quiz_id)
    # yung quiz id pala ay para lang sa quiz for unique indetification hindi siya current user
    # ang current user pala ang magiging author
    if category == '1':
        form = MatchingTypeForm()    
        return render_template('questionaire.html', form=form, quiz_id=quiz_id, category=category)
    elif category == '2':
        form = FillInTheBlanksForm()
        return render_template('questionaire.html', form=form, quiz_id=quiz_id, category=category)
    elif category =='3':
        form = TrueOrFalseForm()
        return render_template('questionaire.html', form=form, quiz_id=quiz_id, category=category)
    else:
        return render_template('404.html')


@views.route('/matchingtype', methods=['GET', 'POST'])
@login_required
def matchingtype():

    form = MatchingTypeForm()
    if form.validate_on_submit():
        question = form.question.data
        choice1 = form.choice1.data
        choice2 = form.choice2.data
        choice3 = form.choice3.data
        choice4 = form.choice4.data
        answer = form.answer.data

        matchingtype  = MatchingType(quiz_id=current_user.id , question=question, choice1=choice1, choice2=choice2, choice3=choice3, choice4=choice4, answer=answer)
        db.session.add(matchingtype)
        db.session.commit()
        flash('Your question has been added!', 'success')
        return redirect(url_for('views.questionaire', current_user.id , category='1'))

    return render_template('questionaire.html', form=form, quiz_id=current_user.id, category='1')

@views.route('/fillintheblanks', methods=['GET', 'POST'])
@login_required
def fillintheblanks():
    form = FillInTheBlanksForm()
    if form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data
        fillintheblanks = FillInTheBlanks(quiz_id=current_user.id , question=question, answer=answer)
        db.session.add(fillintheblanks)
        db.session.commit()
        flash('Your question has been added!', 'success')
        return redirect(url_for('views.fillintheblanks', quiz_id=current_user.id , category='2'))
    
    return render_template('questionaire.html', form=form, quiz_id=current_user.id , category='2')


@views.route('/trueorfalse', methods=['GET', 'POST'])
@login_required
def trueorfalse():
    form = TrueOrFalseForm()

    if form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data

        if answer == '0':
            answer = False
        else:
            answer = True
        TOF = TrueOrFalse(quiz_id=current_user.id , question=question, answer=answer)
        db.session.add(TOF)
        db.session.commit()

        flash('Your question has been added!', 'success')
        return redirect(url_for('views.questionaire', quiz_id=current_user.id , category=3))
    


@views.route('/images/<filename>')
@login_required
def images(filename):
    return  send_from_directory("images", filename)





@views.route('/quizbank')
@login_required
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

