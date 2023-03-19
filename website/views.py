#routes 
from flask import Blueprint, render_template, url_for, flash, redirect, send_from_directory, jsonify, request, Response
from datetime import datetime, time
from flask_login import login_required, current_user
from .models import User, QuizList, MatchingType, FillInTheBlanks, TrueOrFalse, Violations
from .forms import CreateQuiz, MatchingTypeForm, FillInTheBlanksForm, TrueOrFalseForm
from .utils import generate_random_string, activity_logs
from .import db

import os
from website.detection import gen
from os import path
import torch
import io
from PIL import Image
import cv2
import numpy as np
from io import BytesIO
import torch
import pandas
import time
import mediapipe as mp

views = Blueprint('views', __name__)

violations = {
    'detected' : 'Nothing is detected',
    'multiple_people' : 'Nothing is detected',
    'phone_detected' : 'No Phone is detected',
    'focus' : 'Nothing is detected',
    'switch_tabs' : 'Nothing is detected',
    'detection_time': 'Not set yet'
}

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)


def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', 'yolov5s.pt')
    model.eval()
    model.cpu()
    model.conf = 0.6  # confidence threshold (0-1)
    model.iou = 0.5  # NMS IoU threshold (0-1) 
    model.nms = 0.1
    #model.classes = [0, 2, 3, 5, 6, 7]
    return model

@views.route("/video")
@login_required
def video():
    model = load_model()
    return Response(gen(model),mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(model):
    cap=cv2.VideoCapture(0)
    # Read until video is completed
    frame_count = 0 
    total_fps = 0 
    while(cap.isOpened()):
        
        # Capture frame-by-fram ## read the camera frame
        success, frame = cap.read()
        #frame = cv2.flip(frame, 1)
        if success == True:

            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()
            
            img = Image.open(io.BytesIO(frame))   
            #pose_estimation(frame)

            current_detection = ""
            
            image = np.array(Image.open(io.BytesIO(frame)))
            output = face_mesh.process(image)
            
            # To improve performance
            image.flags.writeable = True
            
            # Convert the color space from RGB to BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            img_h, img_w, img_c = image.shape
            face_3d = []
            face_2d = []

            if output.multi_face_landmarks:
                for face_landmarks in output.multi_face_landmarks:
                    for idx, lm in enumerate(face_landmarks.landmark):
                        if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                            if idx == 1:
                                nose_2d = (lm.x * img_w, lm.y * img_h)
                                nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                            x, y = int(lm.x * img_w), int(lm.y * img_h)

                            # Get the 2D Coordinates
                            face_2d.append([x, y])

                            # Get the 3D Coordinates
                            face_3d.append([x, y, lm.z])       
                    
                    # Convert it to the NumPy array
                    face_2d = np.array(face_2d, dtype=np.float64)

                    # Convert it to the NumPy array
                    face_3d = np.array(face_3d, dtype=np.float64)

                    # The camera matrix
                    focal_length = 1 * img_w

                    cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                            [0, focal_length, img_w / 2],
                                            [0, 0, 1]])

                    # The distortion parameters
                    dist_matrix = np.zeros((4, 1), dtype=np.float64)

                    # Solve PnP
                    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                    # Get rotational matrix
                    rmat, jac = cv2.Rodrigues(rot_vec)

                    # Get angles
                    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                    # Get the y rotation degree
                    x = angles[0] * 360
                    y = angles[1] * 360
                    z = angles[2] * 360
                

                    # See where the user's head tilting
                    if y < -10:
                        # i want to know how long this guy been looking to his left or right or up or down
                        #text = "Looking Left"
                        current_detection = 'Left'
                        #print(current_detection)
                    elif y > 10:
                        current_detection = 'Right'
                        #print(current_detection)
                    elif x < -10:
                        current_detection = "Looking Down"
                        #print(current_detection)
                    elif x > 10:
                        current_detection = "Looking Up"
                        #print(current_detection)
                    else:
                        current_detection = "Front"
                        #print(current_detection)

                    # Display the nose direction
                    nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)
            
            start_time = time.time()
            results = model(img, size=412)
            rl = results.xyxy[0].tolist()
            
            forward_end_time = time.time()
            forward_pass_time = forward_end_time - start_time
            # Get the current fps.
            fps = 1 / (forward_pass_time)
            # Add `fps` to `total_fps`.
            total_fps += fps
            # Increment frame count.
            frame_count += 1

            for  detection in rl:
                if detection[5] == 0:
                    # current_detection = 'left'
                    violations["detected"] = "The user keep looking to the back"
                    yolo_detection = violations["detected"]
                    print(violations["detected"])
                    #data_recorded(detection=violations["detected"])
                    #check_detection
                    # record_data()
                    # check_detection(current_detection, counter)
                    # counter = 1
                elif detection[5] == 1:
                    violations["detected"] = "The user is focus"
                    yolo_detection = violations["detected"]
                    #data_recorded(detection=violations["detected"])
                    print(violations["detected"])
                elif detection[5] == 2:
                    violations["detected"] = "The user keep looking to the Frontleft"
                    yolo_detection = violations["detected"]
                    #data_recorded(detection=violations["detected"])
                    print(violations["detected"])
                elif detection[5] == 3:
                    violations["detected"] = "The user keep looking to the FrontRight"
                    yolo_detection = violations["detected"]
                    #data_recorded(detection=violations["detected"])
                    print(violations["detected"])
                elif detection[5] == 4:
                    violations["detected"] = "The user keep looking to the left"
                    yolo_detection = violations["detected"]
                    #data_recorded(detection=violations["detected"])
                    print(violations["detected"])
                elif detection[5] == 5:
                    violations["phone_detected"] = "The system detected some phone"
                    yolo_detection = violations["phone_detected"]
                    #data_recorded(detection=violations["detected"])
                    print(violations["phone_detected"])
                elif detection[5] == 6:
                    violations["detected"] = "The user keep looking to the right"
                    yolo_detection = violations["detected"]
                    #data_recorded(detection=violations["detected"])
                    print(violations["detected"])
                elif detection[5]:
                    violations["detected"] = "nothing is detected"
               

            #convert remove single-dimensional entries from the shape of an array
            img = np.squeeze(results.render()) #RGB
            img = annotate_fps(img, fps)
            
            # read image as BGR
            img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) #BGR

            final_end_time = time.time()
            forward_and_annot_time = final_end_time - start_time
            print_string = f"Frame: {frame_count}, Forward pass FPS: {fps:.3f}, "
            print_string += f"Forward pass time: {forward_pass_time:.3f} seconds, "
            print_string += f"Forward pass + annotation time: {forward_and_annot_time:.3f} seconds"
            #print(print_string)  
        else:
            break

        # Encode BGR image to bytes so that cv2 will convert to RGB
        frame = cv2.imencode('.jpg', img_BGR)[1].tobytes()
        #print(frame)
        
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def draw_text(
        img,
        text,
        font=cv2.FONT_HERSHEY_SIMPLEX,
        pos=(0, 0),
        font_scale=1,
        font_thickness=2,
        text_color=(0, 255, 0),
        text_color_bg=(0, 0, 0),
    ):
        offset = (5, 5)
        x, y = pos
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_w, text_h = text_size
        rec_start = tuple(x - y for x, y in zip(pos, offset))
        rec_end = tuple(x + y for x, y in zip((x + text_w, y + text_h), offset))
        cv2.rectangle(img, rec_start, rec_end, text_color_bg, -1)
        cv2.putText(
            img,
            text,
            (x, int(y + text_h + font_scale - 1)),
            font,
            font_scale,
            text_color,
            font_thickness,
            cv2.LINE_AA,
        )
        return img   

def annotate_fps(orig_image, fps_text):
    draw_text(
        orig_image,
        f"FPS: {fps_text:0.1f}",
        pos=(20, 20),
        font_scale=1.0,
        text_color=(204, 85, 17),
        text_color_bg=(255, 255, 255),
        font_thickness=2,
    )
    return orig_image


# passing variable from javascript and python using Ajax
# https://stackoverflow.com/questions/2894946/passing-javascript-variable-to-python
@views.route('/pass_val',methods=['POST'])
@login_required
def pass_val():
    violations['switch_tabs']= request.args.get('value')
    switchtabs = violations['switch_tabs']
    #data_recorded(switch_tabs=violations['switch_tabs'])
    return jsonify({'reply':'success'})

def record_the_detection():
    new_violations = Violations(
            detected=violations['detected'], 
            phone_detected= violations['phone_detected'],
            user_id=current_user.id
        )

@views.route('/quiz1')
def quiz1():
    return render_template('quiz1.html')


@views.route('/records')
@login_required
def records():
    return render_template('records.html', violations=violations, username=current_user.email)


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

