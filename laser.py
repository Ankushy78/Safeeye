import cv2
import numpy as np


KNOWN_OBJECT_WIDTH_CM = 16  
FOCAL_LENGTH_PIXELS = 500  
DISTANCE_THRESHOLD_CM = 40 


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def estimate_distance_from_object_size(object_width_pixels):
    """
    Estimate the distance from the camera based on the object's width in pixels.
    """
    if object_width_pixels == 0:
        return float('inf')  
    distance_cm = (KNOWN_OBJECT_WIDTH_CM * FOCAL_LENGTH_PIXELS) / object_width_pixels
    return distance_cm

def laser_detection_system():
    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    laser_position = 320  
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

       
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

       
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        detected = False
        for (x, y, w, h) in faces:
           
            distance_cm = estimate_distance_from_object_size(w)

            if distance_cm < DISTANCE_THRESHOLD_CM:
                detected = True
                cv2.circle(frame, (laser_position, frame.shape[0] // 2), 10, (0, 0, 255), -1)  # Red circle (laser)

                
                cv2.putText(frame, f"Intruder detected at {distance_cm:.2f} cm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

       
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, f"{distance_cm:.2f} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


        cv2.imshow("Laser Detection System", frame)

        if detected:
            print(f"Intruder detected at {distance_cm:.2f} cm!")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

 
    cap.release()
    cv2.destroyAllWindows()


laser_detection_system()