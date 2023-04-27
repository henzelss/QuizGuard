#routes 
from functools import wraps
from flask import Blueprint, render_template, url_for, flash, redirect, send_from_directory, jsonify, request, Response, session, send_file, json
from website.socketio import socketio
from datetime import datetime, time
from flask_login import login_required, current_user
from .models import User, QuizList, MultipleChoice, FillInTheBlanks, TrueOrFalse, Violations, Student, Room
from .forms import CreateQuiz, MultipleChoiceForm, FillInTheBlanksForm, TrueOrFalseForm, MultipleChoiceFormEdit, FillInTheBlanksFormEdit, TrueOrFalseFormEdit, QuizForm, SearchCode, MultipleChoiceQuizForm 
from .utils import generate_random_string, activity_logs
from .import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date


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
        return redirect(url_for('views.professor'))

    # If the user's usertype is not recognized, redirect to a custom error page
    return render_template('error.html', message='Unknown user type')


@views.route('/student')
@login_required
def student():
    # quiz_list = QuizList.query.all()
    # joined the table so we can show the author fullname
    # form = SearchCode()
    # quiz_list = db.session.query(QuizList, User.firstname, User.lastname).join(User, QuizList.author_id == User.id).all()
    # return render_template('student.html', quiz_list=quiz_list, form=form)

    form = SearchCode()
    current_date = date.today()
    quiz_list = (
        db.session.query(QuizList, User.firstname, User.lastname)
        .join(User, QuizList.author_id == User.id)
        .filter(QuizList.startdate <= current_date)
        .filter(QuizList.enddate >= current_date)
        .all()
    )
    return render_template('student.html', quiz_list=quiz_list, form=form, current_user=current_user)

@views.route('/professor')
def professor():
    return render_template('professor.html', current_user=current_user)


@views.route('/myquiz')
def myquiz():   
    #quiz_list = db.session.query(QuizList).filter_by(author_id=current_user.id).all()
    quiz_list = db.session.query(QuizList, User.firstname, User.lastname)\
        .join(User, QuizList.author_id == User.id)\
        .filter(User.id == current_user.id)\
        .all()
    return render_template('myquiz.html', quiz_list=quiz_list, current_user=current_user)

@views.route('/clonequiz/<string:quizid>/<string:quizcode>', methods=['GET', 'POST'])
def clonequiz(quizid, quizcode):
    # Find the quiz to clone
    quiz = QuizList.query.filter_by(id=quizid).first()

    # Create a new quiz with the same attributes as the original
    new_quiz_code = generate_random_string(8)
    new_quiz = QuizList(author_id=current_user.id,
                        code=new_quiz_code,
                        title=quiz.title,
                        description=quiz.description,
                        category=quiz.category,
                        quiztype=quiz.quiztype,
                        startdate=quiz.startdate,
                        enddate=quiz.enddate,
                        timelimit=quiz.timelimit,
                        points=quiz.points,
                        visibility=quiz.visibility,
                        attempt=quiz.attempt)
    db.session.add(new_quiz)
    db.session.flush()  # generate an id for the new quiz

    # Copy over the questions from the original quiz
    if quiz.quiztype == '1':
        questions = MultipleChoice.query.filter_by(quiz_code=quiz.code).all()
        for question in questions:
            new_question = MultipleChoice(quiz_code=new_quiz.code,
                                          question=question.question,
                                          choice1=question.choice1,
                                          choice2=question.choice2,
                                          choice3=question.choice3,
                                          choice4=question.choice4,
                                          answer=question.answer)
            db.session.add(new_question)
    elif quiz.quiztype == '2':
        questions = FillInTheBlanks.query.filter_by(quiz_code=quiz.code).all()
        for question in questions:
            new_question = FillInTheBlanks(quiz_code=new_quiz.code,
                                           question=question.question,
                                           answer=question.answer)
            db.session.add(new_question)
    elif quiz.quiztype == '3':
        questions = TrueOrFalse.query.filter_by(quiz_code=quiz.code).all()
        for question in questions:
            new_question = TrueOrFalse(quiz_code=new_quiz.code,
                                       question=question.question,
                                       answer=question.answer)
            db.session.add(new_question)

    db.session.commit()
    flash("Successfully clone the quiz", category="success")
    return redirect(url_for('views.myquiz'))

@views.route('/quizbank')
@login_required
def quizbank():
    form = SearchCode()
    # SELECT quiz_list.*, user.firstname, user.lastname 
    # FROM quiz_list 
    # JOIN user ON quiz_list.author_id = user.id;
    quiz_list = db.session.query(QuizList, User.firstname, User.lastname).join(User, QuizList.author_id == User.id).all()
    return render_template('quizbank.html', quiz_list=quiz_list, form=form, current_user=current_user)

# @views.route('/quizbank')
# @login_required
# def quizbank():
#     # user is authenticated, do something
#     # SELECT quiz_list.*, user.firstname, user.lastname 
#     # FROM quiz_list 
#     # JOIN user ON quiz_list.author_id = user.id;
#     form = SearchCode()
#     current_date = date.today()
#     quiz_list = (
#         db.session.query(QuizList, User.firstname, User.lastname)
#         .join(User, QuizList.author_id == User.id)
#         .filter(QuizList.startdate <= current_date)
#         .filter(QuizList.enddate >= current_date)
#         .all()
#     )
#     print(f'quiz_list : {quiz_list}')

#     return render_template('quizbank.html', quiz_list=quiz_list, form=form, current_user=current_user)

@views.route('/searchquiz',  methods=['GET', 'POST'])
@login_required
def searchquiz():
    form = SearchCode()
    if form.validate_on_submit():
        code = form.search.data
        #quiz = QuizList.query.filter_by(code=code).first()
        quiz = db.session.query(QuizList).filter_by(code=code).first()
        if quiz:
            author = User.query.filter_by(id=quiz.author_id).first()
            return render_template('searchbank.html', quiz=quiz, form=form, author=author, current_user=current_user)
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
    quizform.quizcode.data = quizcode
    if quiztype == '1':
        form = MultipleChoiceFormEdit()
        questions = MultipleChoice.query.join(QuizList).filter(QuizList.code == quizcode).all()
    elif quiztype == '2':
        form = FillInTheBlanksForm()
        questions = FillInTheBlanks.query.join(QuizList).filter(QuizList.code == quizcode).all()
    elif quiztype == '3': 
        form = TrueOrFalseFormEdit()
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

@views.route('/myquizdelete/<string:quiz_code>/<string:quiztype>', methods=['GET', 'POST'])
@login_required
def myquizdelete(quiz_code, quiztype):
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
    flash('Quiz is successfully removed', category='success')
    activity_logs('Deleted a quiz')
    return redirect(url_for('views.myquiz'))

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

        if quiztype == '3':
            answer = form.answer.data

            if answer == '0':
                question.answer = True
            else:
                question.answer = False
        
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
            question = form.question.data
            answer = None  # initialize the variable to None
            if form.answer.data == '1':
                answer = True
            else:
                answer = False
            question = TrueOrFalse(
                question=question,
                answer=answer,
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

@views.route('/editquiz<string:quizcode>/<string:quiztype>/', methods=['GET', 'POST'])
@login_required
def editquiz(quizcode, quiztype):
    if current_user.usertype == 'user':
        flash('You dont have permission to access this page', category='error')
        activity_logs("Try to access webpages not for users")
        return redirect(url_for('views.student'))
    
    quiz = QuizList.query.filter_by(code=quizcode).first()
    if not quiz:
        flash('Quiz not found!', category='error')
        return redirect(url_for('views.quizbank'))
    
    form = QuizForm(obj=quiz)

    if request.method == 'POST' and request.form.get('submit'):
        startdate_str = request.form['startdate']
        startdate = datetime.strptime(startdate_str, '%Y-%m-%d').date()

        enddate_str = request.form['enddate']
        enddate = datetime.strptime(enddate_str, '%Y-%m-%d').date()



        form.populate_obj(quiz)
        quiz.startdate = startdate
        quiz.enddate = enddate

        db.session.commit()
        print(quizcode)
        print(quiztype)
        activity_logs('Updated Quiz')
        flash('Quiz updated successfully!', category='success')
        return redirect(url_for('views.quizbankedit', quizcode=quizcode, quiztype=quiztype))

    return redirect(url_for('views.quizbankedit', quizcode=quizcode, quiztype=quiztype))

# @views.route('/deletequiz<string:quizcode>', methods=['GET', 'POST'])
# @login_required
# def DeleteQuiz():
#     if current_user.usertype == 'user':
#         flash('You dont have permission to access this page', category='error')
#         activity_logs("Try to access webpages not for users")
#         return redirect(url_for('views.student'))
    
#     pass
@views.route('/createquiz', methods=['GET', 'POST'])
@login_required
def createquiz():
    if current_user.usertype == 'user':
        flash('You dont have permission to access this page', category='error')
        activity_logs("Try to access webpages not for users")
        return redirect(url_for('views.student'))

    form = QuizForm()
    if request.method == 'GET':
        new_code = generate_random_string(8)
        form.quizcode.data = new_code
        print('generated code: ' + new_code)
    elif request.method == 'POST' and request.form.get('submit'):

        startdate_str = request.form['startdate']
        startdate = datetime.strptime(startdate_str, '%Y-%m-%d').date()

        enddate_str = request.form['enddate']
        enddate = datetime.strptime(enddate_str, '%Y-%m-%d').date()

        new_quiz = QuizList(
            author_id=current_user.id,
            code=form.quizcode.data,
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            quiztype=form.quiztype.data,
            startdate=startdate,
            enddate=enddate,
            timelimit=form.timelimit.data,
            points=form.points.data,
            visibility=form.visibility.data,
            attempt=form.attempt.data
        )

        db.session.add(new_quiz)
        db.session.commit()
        activity_logs('Added New Quiz')
        flash('New quiz successfully added!', category='success')
        return redirect(url_for('views.quizbankedit', quizcode=form.quizcode.data, quiztype=form.quiztype.data))
    
    return render_template('createquiz.html', form=form)


@views.route('/checkcamera/<string:quizid>/<string:quizcode>/<string:quiztype>', methods=['GET', 'POST'])
@login_required
def checkcamera(quizid, quizcode, quiztype):
    # pwede i load model dito
    return render_template('check_camera.html', quizid=quizid, quizcode=quizcode, quiztype=quiztype)

@views.route('/quiz/<string:quizid>/<string:quizcode>/<string:quiztype>', methods=['GET', 'POST'])
@login_required
def quiz(quizid, quizcode, quiztype):
    
    room = Room.query.filter_by(quiz_code=quizcode, user_id=current_user.id).first()
    if not room:
        # If not, create a new Room object and add it to the database
        room = Room(quiz_code=quizcode, user_id=current_user.id, toast_message="", status="active")
        db.session.add(room)
        db.session.commit()
        
    quiz = QuizList.query.filter_by(code=quizcode).first()
    if quiz is None:
        # handle invalid quiz code
        flash("Invalid Quiz Code ", category="error")
        return redirect(url_for('views.student'))
    questions = None
    if quiztype == '1':
        #form = MultipleChoiceQuizForm()
        questions = MultipleChoice.query.filter_by(quiz_code=quizcode).all()
    elif quiztype == '2':
        #form = FillInTheBlanksForm()
        questions = FillInTheBlanks.query.filter_by(quiz_code=quizcode).all()
    elif quiztype == '3':
        #form = TrueOrFalseForm()
        questions = TrueOrFalse.query.filter_by(quiz_code=quizcode).all()

    if questions is None or len(questions) == 0:
        print('question len is none')
        flash("No questions found for this quiz", category="error")
        return redirect(url_for('views.student'))
    else: 
        print('question len is not none')
        question_count = len(questions)
        return render_template('quiz.html', quiz=quiz, questions=questions, quiztype=quiztype, quizcode=quizcode, question_count=question_count)

    # question_count = len(questions)
    # return render_template('quiz.html', quiz=quiz, questions=questions, quiztype=quiztype, quizcode=quizcode, question_count=question_count)

@views.route('/result/<string:quizcode>/<string:quiztype>', methods=['GET', 'POST'])
@login_required
def result(quizcode, quiztype ):
    #violations = Violations.query.all()
    violations = db.session.query(User.id, User.firstname, User.lastname, Violations.laptop, Violations.phone, Violations.head_pose, Violations.switch_tabs).\
                join(Violations, User.id == Violations.user_id).\
                join(QuizList, QuizList.code == Violations.quiz_code).\
                filter(Violations.user_id == current_user.id).\
                filter(QuizList.code == quizcode).all()
    score = 0
    total_no_question = 0
    if request.method =="POST" or request.form.get('submit') == 'Submit':
        for question in request.form:
            print(question)
            if question.startswith('student_answer'):
                print(question)
                question_id = question.replace('student_answer', '')
                print("question id: " + question_id)
                if quiztype == '1':
                    selected_answer = request.form[question] #getting the answers
                    correct_answer = MultipleChoice.query.filter_by(id=question_id).first().answer
                    if selected_answer == correct_answer:
                        score += 1
                elif quiztype == '2':
                    student_answer = request.form[question] #getting the answers
                    correct_answer = FillInTheBlanks.query.filter_by(id=question_id).first().answer
                    print("Student Answer: " + student_answer.strip().lower())
                    print("Corrent Answer: " + correct_answer.strip().lower())
                    if student_answer.strip().lower() == correct_answer.strip().lower():
                        score += 1
                elif quiztype == '3':
                    student_answer = request.form[question] #getting the answers
                    correct_answer = TrueOrFalse.query.filter_by(id=question_id).first().answer
                    if student_answer.lower() == str(correct_answer).lower():
                        score += 1
            else:
                print("error")
        total_no_question = int(request.form['total_no_question'])
        quiz = QuizList.query.filter_by(code=quizcode).first()
        score = score * quiz.points
        total_score = total_no_question * quiz.points   
        existing_student = Student.query.filter_by(user_id=current_user.id, quiz_id=quiz.id).first()
        if existing_student:
            existing_student.score = score
        else:
            student = Student(user_id=current_user.id, quiz_id=quiz.id, score=score)
            db.session.add(student)
        db.session.commit()
        # student = Student(user_id=current_user.id, quiz_id=quiz.id, score=score)
        # db.session.add(student)
        # db.session.commit()
        # Delete student from room table
        #joined table of user and student table
        room_student = Room.query.filter_by(user_id=current_user.id).first()
        if room_student:
            db.session.delete(room_student)
            db.session.commit()

        students = db.session.query(Student.score, User.firstname, User.lastname).\
          join(User, Student.user_id==User.id).\
          filter(Student.quiz_id == quiz.id).\
          order_by(Student.score.desc()).\
          all()
        return render_template('result.html', students=students, quiz=quiz, violations=violations, total_score=total_score)
    # else:
    #     # quiz = QuizList.query.filter_by(code=quizcode).first()
    #     # total_no_question = quiz.questions.count()
    #     # student = Student.query.filter_by(user_id=current_user.id, quiz_id=quiz.id).first()
    #     # if student:
    #     #     score = student.score
    #     # return render_template('result.html', students=students, quiz=quiz, violations=violations, total_no_question=total_no_question, score=score)
    #     return


@views.route('/record_prediction', methods=['POST'])
@login_required
def process_frame():
    prediction_class = request.form.get("prediction_class")
    if prediction_class:
        # check if the user already has a violation of this type
        violation = Violations.query.filter_by(user_id=current_user.id, detected=prediction_class).first()
        if violation:
            # update the existing violation
            violation.date = datetime.now()
        else:
            # create a new violation
            violation = Violations(
                detected=prediction_class,
                user_id=current_user.id
            )
        # check if the prediction class is "phone"
        if prediction_class == "phone":
            violation.phone_detected = "Yes"
        # save the violation to the database
        try:
            db.session.add(violation)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "failed"
        return "success"
    else:
        return "failed"

# @views.route('/switchtabs',methods=['POST'])
# @login_required
# def switchtabs():
#     value = request.args.get('value')
#     user_id = current_user.id
#     violation = Violations.query.filter_by(user_id=user_id).first()
#     if violation is not None:
#         violation.switch_tabs = value
#         db.session.commit()
#     else:
#         violation = Violations(switch_tabs=value, user_id=user_id)
#         db.session.add(violation)
#         db.session.commit()
#     return jsonify({'reply': 'success'})

@views.route('/switchtabs', methods=['POST'])
@login_required
def switchtabs():
    value = request.args.get('value')
    user_id = current_user.id
    quiz_code = request.args.get('quiz_code')
    violation = Violations.query.filter_by(user_id=user_id, quiz_code=quiz_code).first()
    if violation is not None:
        violation.switch_tabs = value
        db.session.commit()
    else:
        violation = Violations(switch_tabs=value, user_id=user_id, quiz_code=quiz_code)
        db.session.add(violation)
        db.session.commit()
    return jsonify({'reply': 'success'})




# this is function is for bulk entry of questions for multiple choice type quiz        
@views.route('/upload_multiple/<string:quizcode>/<string:quiztype>', methods=['POST'])
@login_required
def upload_multiple(quizcode, quiztype):
    file = request.files['file']
    if file.filename.endswith('.txt'):
        contents = file.read()
        questions = json.loads(contents)
        for question in questions:
            multiple_choice = MultipleChoice( quiz_code=quizcode, 
                                             question=question['question'], 
                                             choice1=question['choice1'], 
                                             choice2=question['choice2'], 
                                             choice3=question['choice3'],
                                             choice4=question['choice4'],
                                             answer=question['answer'])
            db.session.add(multiple_choice)

        db.session.commit()
        flash("Questions uploaded successfully", category="success")
        return redirect(url_for('views.quizbankedit', quizcode=quizcode, quiztype=quiztype))
    else:
        flash("Unsuccessfull insert please check the format or the file type", category="warning")
        return redirect(url_for('views.quizbankedit', quizcode=quizcode, quiztype=quiztype))

# this is function is for bulk entry of questions for fill in the blank type quiz
@views.route('/upload_fob/<string:quizcode>/<string:quiztype>', methods=['POST'])
@login_required
def upload_fob(quizcode, quiztype):
    # get the file
    file = request.files['file']
    # check if the file endswith .txt
    if file.filename.endswith('.txt'):
        # read the contents of the file
        contents = file.read()
        # questions = [ {}, {}] is equal to a list of dictionary
        questions = json.loads(contents)
        # now loop to the list
        for question in questions:
            # place the question and answer to the table to be inserted
            fill_in_the_blanks = FillInTheBlanks( quiz_code=quizcode, question=question['question'], answer=question['answer'])
            # the the question 
            db.session.add(fill_in_the_blanks)
            #then repeat until it ends 

        # commit the changes to the table
        db.session.commit()
        # flash the message
        flash("Questions uploaded successfully", category="success")
        # redirect the user back to the quizbankedit
        return redirect(url_for('views.quizbankedit', quizcode=quizcode, quiztype=quiztype))
    else:
        # if the user didnt upload anything or upload a wrong file
        flash("Invalid File Type", category="warning")
        # redirect the user back to the quizbankedit
        return redirect(url_for('views.quizbankedit', quizcode=quizcode, quiztype=quiztype))

@views.route('/upload_tor/<string:quizcode>/<string:quiztype>', methods=['POST'])
@login_required
def upload_tor(quizcode, quiztype):
   
    file = request.files['file']
    if file.filename.endswith('.txt'):

        contents = file.read()
        print()
        questions = json.loads(contents)
        for question in questions:
            answer = None
            if question['answer'] == 0:
                answer = True
            else:
                answer = False 
            true_or_false = TrueOrFalse(
                            quiz_code=quizcode,
                            question=question['question'],
                            answer=answer
                        )
            db.session.add(true_or_false)

        db.session.commit()
        flash("Questions uploaded successfully", category="success")
        return redirect(url_for('views.quizbankedit', quizcode=quizcode, quiztype=quiztype))
    else:
        flash("Invalid File Type", category="warning")
        return redirect(url_for('views.quizbankedit', quizcode=quizcode, quiztype=quiztype))



@views.route('/top5')
def top5():
    pass

@views.route('/top10')
def top10():
    pass

@views.route('/ExportAllResult')
def ExportAllResult():
    pass



@views.route('/monitoring/<string:quizcode>')
@login_required
def monitoring(quizcode):
    room_query = db.session.query(Room, User.id, User.firstname, User.lastname, Violations.laptop, Violations.phone, Violations.head_pose, Violations.switch_tabs, QuizList.code)\
        .select_from(Room)\
        .join(User, Room.user_id == User.id)\
        .join(Violations, (Room.user_id == Violations.user_id) & (Room.quiz_code == Violations.quiz_code))\
        .join(QuizList, QuizList.code == Room.quiz_code)\
        .filter(Room.quiz_code == quizcode, Room.user_id != current_user.id)\
        .all()

    current_room = []
    if room_query is not None:
        for room, user_id, firstname, lastname, laptop, phone, head_pose, switch_tabs, quiz_code in room_query:
            current_room.append({'user_id': user_id, 'firstname': firstname, 'lastname': lastname, 'laptop': laptop, 'phone': phone, 'head_pose': head_pose, 'switch_tabs': switch_tabs, 'quiz_code': quiz_code})
            # Your code to pass the query results to the template goes here
    else:
        flash("The room is currently empty right now ", category='warning')
        return redirect(url_for('views.quizbank'))
    flash("This is the current user inside the quiz", category="success")
    return render_template('monitoring.html', current_room=current_room)

#multiple choice
@views.route('/download_multiple/')
@login_required
def download_multiple():
    filepath = '../data/multiple.txt'
    return send_file(filepath, as_attachment=True)

#fill in the blanks
@views.route('/download_fob')
@login_required
def download_fob():
    filepath = '../data/fob.txt'
    return send_file(filepath, as_attachment=True)

# true or false
@views.route('/download_tor')
@login_required
def download_tor():
    filepath = '../data/tor.txt'
    return send_file(filepath, as_attachment=True)



@views.route('/send_message/<string:quizcode>/<int:userid>', methods=['POST'])
def send_message(quizcode, userid):
    # Get the quiz code and user ID
    quiz_code = quizcode
    userid = userid
    message = request.form.get('message')
    # Get the current room for the quiz and user
    room = Room.query.filter_by(quiz_code=quiz_code, user_id=userid).first()
    if room:
        room.toast_message = message
    else:
        room = Room(user_id=userid, toast_message=message, status='active')
        db.session.add(room)
    
    db.session.commit()
    # Send message to the user asynchronously
    socketio.emit('toast_message', {'message': room.toast_message}, room=userid)
    
    return redirect(url_for('views.monitoring',  quizcode=quizcode)), 204

@views.route('/records')
@login_required
def records():
    violations = Violations.query.all()
    return render_template("records.html", violations=violations)

@views.route('/images/<filename>')
@login_required
def images(filename):
    return  send_from_directory("images", filename)

@views.route('/error')
@login_required
def error():
    return render_template('error.html')

#error page handler | page not found
@views.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#error page handler | Internal server error
@views.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

