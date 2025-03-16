import cv2
import numpy as np
import time
import face_recognition
import os
import tkinter as tk
from tkinter import messagebox
import winsound


authorized_faces = []
authorized_names = []
authorized_path = "C:\\Users\\PRANAY\\OneDrive\\Desktop\\PROJECTS\\proj\\Photos\\Pranay"

if os.path.exists(authorized_path):
    for filename in os.listdir(authorized_path):
        img_path = os.path.join(authorized_path, filename)
        image = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(image)
        if encoding:
            authorized_faces.append(encoding[0])
            authorized_names.append(os.path.splitext(filename)[0])
else:
    print("Error: Authorized path not found!")


cap = cv2.VideoCapture(0)


unauthorized_timer = None
alert_threshold = 5  


def show_alert():
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Security Alert", "Unauthorized person detected in restricted area!")
    winsound.Beep(1000, 1000)  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_height, frame_width, _ = frame.shape
    middle_x = frame_width // 2
    
   
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
   
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
       
        face_distances = face_recognition.face_distance(authorized_faces, face_encoding)
        best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else -1
        
        name = "Unauthorized"
        if best_match_index != -1 and face_distances[best_match_index] < 0.5:  
            name = authorized_names[best_match_index]
        
        
        color = (0, 255, 0) if name != "Unauthorized" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
       
        if name == "Unauthorized" and right > middle_x:
            if unauthorized_timer is None:
                unauthorized_timer = time.time()
            elif time.time() - unauthorized_timer > alert_threshold:
                print("ALERT: Unauthorized person detected in restricted area!")
                show_alert()
        else:
            unauthorized_timer = None  
    
    
    cv2.line(frame, (middle_x, 0), (middle_x, frame_height), (255, 255, 255), 2)
    cv2.putText(frame, "Restricted Area", (middle_x + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    
    cv2.imshow('Face Recognition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()