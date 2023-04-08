#routes 
from flask import Blueprint, render_template, url_for, flash, redirect, send_from_directory, jsonify, request, Response
from datetime import datetime, time
from flask_login import login_required, current_user
from .models import User, QuizList, MultipleChoice, FillInTheBlanks, TrueOrFalse, Violations
from .forms import CreateQuiz, MultipleChoiceForm, FillInTheBlanksForm, TrueOrFalseForm, MultipleChoiceFormEdit, FillInTheBlanksFormEdit, TrueOrFalseFormEdit, QuizForm, SearchCode
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
        return redirect(url_for('views.student'))
    elif current_user.usertype == 'admin':
        return render_template('admin.html')
    elif current_user.usertype == 'professor':
        return render_template('professor.html')

    # If the user's usertype is not recognized, redirect to a custom error page
    return render_template('error.html', message='Unknown user type')


@views.route('/student')
def student():
    #quiz_list = QuizList.query.all()
    # joined the table so we can show the author fullname
    quiz_list = db.session.query(QuizList, User.firstname, User.lastname).join(User, QuizList.author_id == User.id).all()
    return render_template('student.html', quiz_list=quiz_list)

@views.route('/quizbank')
@login_required
def quizbank():
    form = SearchCode()
    quiz_list = db.session.query(QuizList, User.firstname, User.lastname).join(User, QuizList.author_id == User.id).all()
    return render_template('quizbank.html', quiz_list=quiz_list, form=form)

@views.route('/searchquiz',  methods=['GET', 'POST'])
def searchquiz():
    form = SearchCode()
    if form.validate_on_submit():
        code = form.search.data
        quiz = QuizList.query.filter_by(code=code).first()
        if quiz:
            author = User.query.filter_by(id=quiz.author_id).first()
            return render_template('searchbank.html', quiz=quiz, form=form, author=author)
        else:
            flash('Quiz not found', category='error')
            return redirect(url_for('views.quizbank'))
    return render_template('searchbank.html', form=form)

@views.route('/quizbankedit/<string:quizcode>/<string:quiztype>/', methods=['GET', 'POST'])
@login_required
def quizbankedit(quizcode, quiztype):

    if current_user.usertype == 'user':
        flash('You dont have permission to access this page', category='error')
        return redirect(url_for('views.student'))
    
    quizform = QuizForm()
    if quiztype == '1':
        form = MultipleChoiceFormEdit()
        questions = MultipleChoice.query.join(QuizList).filter(QuizList.code == quizcode).all()
    elif quiztype == '2':
        form = FillInTheBlanksForm()
        questions = FillInTheBlanks.query.join(QuizList).filter(QuizList.code == quizcode).all()
    elif quiztype == '3': 
        form = TrueOrFalseForm()
        questions = TrueOrFalse.query.join(QuizList).filter(QuizList.code == quizcode).all()
    else:
        flash('Quiz code not found', category='warning')
        return redirect(url_for('views.quizbank'))
    
    if not questions:
        flash('No questions has found for this quiz', category='warning')
        
    return render_template('quizbankedit.html', questions=questions, form=form, quiztype=quiztype, quizform=quizform, quizcode=quizcode)

@views.route('/quizbankdelete/<string:quiz_code>/<string:quiztype>', methods=['GET', 'POST'])
@login_required
def quizdelete(quiz_code, quiztype):
    quiz = QuizList.query.filter_by(code=quiz_code).first()
    print(quiz)
    if not quiz:
        flash('Quiz not found', category='error')
        activity_logs('Deleting Non-existing Quiz')
        return redirect(url_for('views.quizbank'))

    if quiztype == '1':
        # Delete all the matching type questions with quiz_code equal to the deleted quiz's code
        multiple_choice = MultipleChoice.query.filter_by(quiz_code=quiz_code).all()
        for question in multiple_choice:
            db.session.delete(question)
    elif quiztype == '2':
        fib_questions = FillInTheBlanks.query.filter_by(quiz_code=quiz_code).all()
        for question in fib_questions:
            db.session.delete(question)
    elif quiztype == '3':
        tor_questions = TrueOrFalse.query.filter_by(quiz_code=quiz_code).all()
        for question in tor_questions:
            db.session.delete(question)

    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz is deleted', category='success')
    activity_logs('Deleted a quiz')
    return redirect(url_for('views.quizbank'))



@views.route('/quizedit/<string:id>/<string:quiztype>/<string:questionid>', methods=['GET', 'POST'])
@login_required
def quizedit(id, quiztype):
    if current_user.usertype == 'user':
        return redirect(url_for('views.student'))
    
    # form = None
    # if quiztype == '1':
    #     form = MatchingTypeFormEdit()
    # elif quiztype == '2':
    #     form = FillInTheBlanksFormEdit()
    # elif quiztype == '3':
    #     form = TrueOrFalseFormEdit()
    # else:
    #     return render_template(url_for('views.dashboard'))


    # # saan galing yung id?
    # if form.validate_on_submit():
    #     if quiztype == '1':
    #         pass
    #     elif quiztype == '2':
    #         pass
    #     elif quiztype == '3':
    #         pass
    #     else:
    #         return render_template(url_for('views.dashboard'))

@views.route('/editquestions<string:quizcode>/<string:quiztype>/<string:questionid>', methods=['GET', 'POST'])
@login_required
def editquestions(quizcode, quiztype, questionid):
    if current_user.usertype == 'user':
        flash('You dont have permission to access this page', category='error')
        activity_logs("Try to access webpages not for users")
        return redirect(url_for('views.student'))

    if quiztype == '1':
        question = MultipleChoice.query.get(questionid)
        form = MultipleChoiceFormEdit(obj=question)
    elif quiztype == '2':
        question = FillInTheBlanks.query.get(questionid)
        form = FillInTheBlanksFormEdit(obj=question)
    elif quiztype == '3':
        question = TrueOrFalse.query.get(questionid)
        form = TrueOrFalseFormEdit(obj=question)
    else:
        flash('Quiz Type doesnt exists', category='error')
        return redirect(url_for('views.quizbankedit'))
    
    if form.validate_on_submit():
        form.populate_obj(question)
        db.session.commit()
        flash('Question updated successfully', category='success')
        return redirect(url_for('views.quizbankedit', quizcode=quizcode, quiztype=quiztype))
    
    return render_template('quizbankedit.html', form=form)

@views.route('/deletequestion<string:quizcode>/<string:quiztype>/<string:questionid>', methods=['GET', 'POST'])
@login_required
def deletequestion(quizcode, quiztype, questionid):
    if current_user.usertype == 'user':
        flash('You dont have permission to access this page', category='error')
        activity_logs("Try to access webpages not for users")
        return redirect(url_for('views.student'))
    
    if quiztype == '1':
        question = MultipleChoice.query.get(questionid)
    elif quiztype == '2':
        question = FillInTheBlanks.query.get(questionid)
    elif quiztype == '3':
        question = TrueOrFalse.query.get(questionid)
    else:
        flash('Invalid Quiz Type', category='error')
        return redirect(url_for('views.quizbankedit', quizcode=quizcode, quiztype=quiztype))
    
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully', category='success')
    return redirect(url_for('views.quizbankedit', quizcode=quizcode, quiztype=quiztype))
    
@views.route('/addquestions<string:quizcode>/<string:quiztype>', methods=['GET', 'POST'])
@login_required
def addquestions(quizcode, quiztype):
    if current_user.usertype == 'user':
        flash('You dont have permission to access this page', category='error')
        activity_logs("Try to access webpages not for users")
        return redirect(url_for('views.student'))
    
    if quiztype == '1':
        form = MultipleChoiceFormEdit()
    elif quiztype == '2':
        form = FillInTheBlanksFormEdit()
    elif quiztype == '3':
        form = TrueOrFalseFormEdit()
    else:
        flash('Invalid Quiz Type', category='error')
        return redirect(url_for('views.quizbankedit'))
    
    if form.validate_on_submit():
        if quiztype == '1':
            question = MultipleChoice(
                question=form.question.data,
                choice1=form.choice1.data,
                choice2=form.choice2.data,
                choice3=form.choice3.data,
                choice4=form.choice4.data,
                answer=form.answer.data,
                quiz_code=quizcode
            )
        elif quiztype == '2':
            question = FillInTheBlanks(
                question=form.question.data,
                answer=form.answer.data,
                quiz_code=quizcode
            )
        elif quiztype == '3':
            question = TrueOrFalse(
                question=form.question.data,
                answer=form.answer.data,
                quiz_code=quizcode
            )
        else:
            flash('Invalid Quiz Type', category='error')
            return redirect(url_for('views.quizbankedit'))
        
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully', category='success')
        return redirect(url_for('views.quizbankedit', quizcode=quizcode, quiztype=quiztype))
    
    return redirect(url_for('views.quizbankedit', quizcode=quizcode, quiztype=quiztype))


@views.route('/editquiz<string:quizcode>', methods=['GET', 'POST'])
@login_required
def EditQuiz():
    if current_user.usertype == 'user':
        flash('You dont have permission to access this page', category='error')
        activity_logs("Try to access webpages not for users")
        return redirect(url_for('views.student'))
    pass

@views.route('/deletequiz<string:quizcode>', methods=['GET', 'POST'])
@login_required
def DeleteQuiz():
    if current_user.usertype == 'user':
        flash('You dont have permission to access this page', category='error')
        activity_logs("Try to access webpages not for users")
        return redirect(url_for('views.student'))
    
    pass



@views.route('/createquiz', methods=['GET', 'POST'])
@login_required
def createquiz():

    if current_user.usertype == 'user':
        flash('You dont have permission to access this page', category='error')
        activity_logs("Try to access webpages not for users")
        return redirect(url_for('views.student'))

    #form = CreateQuiz()
    form = QuizForm()
    code = generate_random_string(8)
    form.quizcode.data = code

    if request.method == 'POST' and request.form.get('submit'):

        startdate_str = request.form['startdate']
        startdate = datetime.strptime(startdate_str, '%Y-%m-%d').date()

        # starttime_str = request.form['starttime']
        # starttime = datetime.strptime(starttime_str, '%H:%M').time()
      

        enddate_str = request.form['enddate']
        enddate = datetime.strptime(enddate_str, '%Y-%m-%d').date()

        # time_closed_str = request.form['time_closed']
        # time_closed = datetime.strptime(time_closed_str, '%H:%M').time()

        
        # new_quiz = QuizList(code=code, 
        #                     title=form.title.data, 
        #                     author_id=current_user.id, 
        #                     category=form.category.data, 
        #                     startdate=startdate,
        #                     starttime=starttime,
        #                     enddate=enddate,
        #                     time_closed=time_closed
        #                     )

        new_quiz = QuizList(author_id=current_user.id,
                            code=code,
                            title = form.title.data,
                            description = form.description.data,
                            category = form.category.data,
                            quiztype = form.quiztype.data,
                            startdate = startdate,
                            enddate = enddate,
                            timelimit = form.timelimit.data,
                            points = form.points.data,
                            visibility = form.visibility.data,
                            attempt = form.attempt.data
                            )

        db.session.add(new_quiz)
        db.session.commit()
        activity_logs('Added New Quiz')
        flash('New quiz successfully added!', category='success')
        #quiz id is qu
        return redirect(url_for('views.questionaire', quiz_code=code, category=form.category.data))
    
    return render_template('createquiz.html', form=form)

#i need to change the model to fix everything
# pwede na to ma remove in the future basta sa create quiz route mag papasa ako sa quizbankedit ng quizcode at quiztype
# remove ko nlng yung questionaire pati yung 3 table na html file
# @views.route('/questionaire/<string:quiz_code>/<string:category>', methods=['GET', 'POST'])
# @login_required
# def questionaire(quiz_code, category):
#     quiz = QuizList.query.get(quiz_code)
#     # yung quiz id pala ay para lang sa quiz for unique indetification hindi siya current user
#     # ang current user pala ang magiging author
#     if category == '1':
#         form = MatchingTypeForm()    
#         return render_template('questionaire.html', form=form, quiz_code=quiz_code, category=category)
#     elif category == '2':
#         form = FillInTheBlanksForm()
#         return render_template('questionaire.html', form=form, quiz_code=quiz_code, category=category)
#     elif category =='3':
#         form = TrueOrFalseForm()
#         return render_template('questionaire.html', form=form, quiz_code=quiz_code, category=category)
#     else:
#         return render_template('404.html')
    
# @views.route('/matchingtype<string:quiz_code>', methods=['GET', 'POST'])
# @login_required
# def matchingtype(quiz_code):

#     form = MatchingTypeForm()
#     if form.validate_on_submit():
#         # quiz id is base on author 
#         question = form.question.data
#         choice1 = form.choice1.data
#         choice2 = form.choice2.data
#         choice3 = form.choice3.data
#         choice4 = form.choice4.data
#         answer = form.answer.data

#         matchingtype = MatchingType(quiz_code=quiz_code, question=question, choice1=choice1, choice2=choice2, choice3=choice3, choice4=choice4, answer=answer)
#         db.session.add(matchingtype)
#         db.session.commit()
#         flash('Your question has been added!', 'success')
#         return redirect(url_for('views.questionaire', quiz_code=quiz_code, category='1'))

#     return render_template('questionaire.html', form=form, quiz_code=quiz_code, category='1')

# @views.route('/fillintheblanks/<string:quiz_code>', methods=['GET', 'POST'])
# @login_required
# def fillintheblanks(quiz_code):
#     form = FillInTheBlanksForm()
#     if form.validate_on_submit():
#         question = form.question.data
#         answer = form.answer.data
#         fillintheblanks = FillInTheBlanks(quiz_code=quiz_code , question=question, answer=answer)
#         db.session.add(fillintheblanks)
#         db.session.commit()
#         flash('Your question has been added!', 'success')
#         return redirect(url_for('views.fillintheblanks', quiz_code=quiz_code , category='2'))
    
#     return render_template('questionaire.html', form=form, quiz_code=quiz_code , category='2')


# @views.route('/trueorfalse/<string:quiz_code>', methods=['GET', 'POST'])
# @login_required
# def trueorfalse(quiz_code):
#     form = TrueOrFalseForm()

#     if form.validate_on_submit():
#         question = form.question.data
#         answer = form.answer.data

#         if answer == '0':
#             answer = False
#         else:
#             answer = True
#         TOF = TrueOrFalse(quiz_code=quiz_code , question=question, answer=answer)
#         db.session.add(TOF)
#         db.session.commit()

#         flash('Your question has been added!', 'success')
#         return redirect(url_for('views.questionaire', quiz_code=quiz_code , category=3))
    

@views.route('/images/<filename>')
@login_required
def images(filename):
    return  send_from_directory("images", filename)

@views.route('/error')
@login_required
def error():
    return render_template('error.html')

@views.route('/SearchQuiz')
@login_required
def SearchQuiz():
    return render_template('quizcode.html')

#error page handler | page not found
@views.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#error page handler | Internal server error
@views.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

