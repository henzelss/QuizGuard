import io
import os
from PIL import Image
import cv2
import numpy as np
from io import BytesIO
import torch
import pandas
import time


detection_dictionary = {
"detected": "",
"phone": "",
"multiple_people": ""
}

def gen(model):
    
    cap=cv2.VideoCapture(0)
    # Read until video is completed
    frame_count = 0 
    total_fps = 0 
    while(cap.isOpened()):
        
        # Capture frame-by-fram ## read the camera frame
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if success == True:

            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()
            
            img = Image.open(io.BytesIO(frame))
            start_time = time.time()
            results = model(img, size=412)
            rl = results.xyxy[0].tolist()
            # results = model(img, size=412)
            # results.print()  
            # print(results)
            # print(rl)
            
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
                    detection_dictionary["detected"] = "The user keep looking to the left"
                    print(detection_dictionary["detected"])
                elif detection[5] == 1:
                    detection_dictionary["detected"] = "The user is focus"
                    print(detection_dictionary["detected"])
                elif detection[5] == 2:
                    detection_dictionary["detected"] = "The user keep looking to the Frontleft"
                    print(detection_dictionary["detected"])
                elif detection[5] == 3:
                    detection_dictionary["detected"] = "The user keep looking to the FrontRight"
                    print(detection_dictionary["detected"])
                elif detection[5] == 4:
                    detection_dictionary["detected"] = "The keep looking to the right"
                    print(detection_dictionary["detected"])
                elif detection[5] == 5:
                    detection_dictionary["detected"] = "The back of the head"
                    print(detection_dictionary["detected"])
                elif detection[5] == 6:
                    detection_dictionary["phone"] = "Phone is detected"
                    print(detection_dictionary["phone"])
                else:
                    print("No detection")

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