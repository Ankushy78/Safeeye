import cv2
import numpy as np
import time
import face_recognition
import os


pedestrian_cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")


authorized_faces = []
authorized_names = []
authorized_path = "C:\\Users\\PRANAY\\OneDrive\\Desktop\\PROJECTS\\proj\\Photos\\Pranay"

for filename in os.listdir(authorized_path):
    img_path = os.path.join(authorized_path, filename)
    image = face_recognition.load_image_file(img_path)
    encoding = face_recognition.face_encodings(image)
    if encoding:
        authorized_faces.append(encoding[0])
        authorized_names.append(os.path.splitext(filename)[0])


cap = cv2.VideoCapture(0)


person_timers = {}
time_threshold = 10  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    pedestrians = pedestrian_cascade.detectMultiScale(gray, 1.1, 3)
    
   
    thermal_frame = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    
    current_time = time.time()
    inside_box = False
    
    for (x, y, w, h) in pedestrians:
        person_center = (int(x + w / 2), int(y + h / 2))
        
        if person_center not in person_timers:
            person_timers[person_center] = current_time
        else:
            elapsed_time = current_time - person_timers[person_center]
            if elapsed_time > time_threshold:
           
                face_frame = frame[y:y+h, x:x+w]
                face_encodings = face_recognition.face_encodings(face_frame)
                
                if face_encodings:
                    matches = face_recognition.compare_faces(authorized_faces, face_encodings[0])
                    if True in matches:
                        matched_idx = matches.index(True)
                        name = authorized_names[matched_idx]
                        print(f"✅ Authorized person detected: {name}")
                    else:
                        print("⚠️ Unauthorized person detected inside the area!")
                else:
                    print("⚠️ Unauthorized person detected inside the area!")
           
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Person Detection', frame)
    cv2.imshow('Thermal View', thermal_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()