'''
HIGH SECURITY Face Recognition System
Strict thresholds for door access control
'''

import cv2
import numpy as np
import os
from datetime import datetime

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

# SECURITY SETTINGS - ADJUST THESE FOR YOUR NEEDS
CONFIDENCE_THRESHOLD = 45  # Lower = stricter (recommended: 40-50 for high security)
CONSECUTIVE_FRAMES_REQUIRED = 3  # Must recognize for 3 frames in a row
ACCESS_COOLDOWN = 3  # Seconds between access grants

# User database
names = ['None', 'Sarthak', 'Person2', 'Person3', 'Person4', 'Person5']

# Initialize camera
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

print("\n" + "="*60)
print("HIGH SECURITY FACE RECOGNITION SYSTEM")
print("="*60)
print(f"Confidence Threshold: {CONFIDENCE_THRESHOLD}")
print(f"Required Consecutive Frames: {CONSECUTIVE_FRAMES_REQUIRED}")
print("="*60)
print("\nSystem Status: ACTIVE")
print("Press ESC to exit\n")

# Tracking variables
consecutive_recognitions = {}
last_access_time = {}
access_log = []

while True:
    ret, img = cam.read()
    
    if not ret:
        print("[ERROR] Camera feed lost")
        break
    
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )
    
    current_time = datetime.now()
    
    # Reset consecutive counts if no faces
    if len(faces) == 0:
        consecutive_recognitions = {}
    
    for (x, y, w, h) in faces:
        # Predict identity
        id_result, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        
        # Calculate match percentage
        match_percentage = round(100 - confidence)
        
        # Determine if this is a valid recognition
        if confidence < CONFIDENCE_THRESHOLD:
            # RECOGNIZED
            person_name = names[id_result]
            
            # Track consecutive recognitions
            if person_name not in consecutive_recognitions:
                consecutive_recognitions[person_name] = 1
            else:
                consecutive_recognitions[person_name] += 1
            
            # Check if enough consecutive frames
            if consecutive_recognitions[person_name] >= CONSECUTIVE_FRAMES_REQUIRED:
                # Check cooldown
                if person_name not in last_access_time:
                    last_access_time[person_name] = datetime.min
                
                time_since_last = (current_time - last_access_time[person_name]).total_seconds()
                
                if time_since_last >= ACCESS_COOLDOWN:
                    # ACCESS GRANTED
                    box_color = (0, 255, 0)  # Green
                    status = "ACCESS GRANTED"
                    status_color = (0, 255, 0)
                    
                    # Log access
                    log_entry = f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] ACCESS GRANTED - {person_name}"
                    access_log.append(log_entry)
                    print(log_entry)
                    
                    last_access_time[person_name] = current_time
                    
                    # HERE: Add code to unlock door
                    # Example: GPIO.output(LOCK_PIN, GPIO.HIGH)
                    
                else:
                    # In cooldown period
                    box_color = (0, 165, 255)  # Orange
                    status = "COOLDOWN"
                    status_color = (0, 165, 255)
            else:
                # Still verifying
                box_color = (0, 255, 255)  # Yellow
                status = f"VERIFYING ({consecutive_recognitions[person_name]}/{CONSECUTIVE_FRAMES_REQUIRED})"
                status_color = (0, 255, 255)
        else:
            # NOT RECOGNIZED
            person_name = "UNKNOWN"
            box_color = (0, 0, 255)  # Red
            status = "ACCESS DENIED"
            status_color = (0, 0, 255)
            consecutive_recognitions = {}
            
            # Log failed attempt
            if len(access_log) == 0 or "DENIED" not in access_log[-1]:
                log_entry = f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] ACCESS DENIED - Unknown person"
                access_log.append(log_entry)
                print(log_entry)
        
        # Draw rectangle around face
        cv2.rectangle(img, (x, y), (x+w, y+h), box_color, 3)
        
        # Display name
        cv2.putText(img, person_name, (x+5, y-40), font, 1, (255, 255, 255), 2)
        
        # Display confidence
        cv2.putText(img, f"Match: {match_percentage}%", (x+5, y-10), 
                    font, 0.6, (255, 255, 255), 2)
        
        # Display status at top of screen
        cv2.putText(img, status, (10, 40), font, 1.2, status_color, 3)
        
        # Display security level
        if confidence < CONFIDENCE_THRESHOLD:
            security_text = f"Security: HIGH | Threshold: {CONFIDENCE_THRESHOLD}"
        else:
            security_text = f"Security: HIGH | Below threshold by {round(confidence - CONFIDENCE_THRESHOLD)}"
        cv2.putText(img, security_text, (10, 470), font, 0.5, (255, 255, 255), 1)
    
    # Show frame
    cv2.imshow('SECURE ACCESS CONTROL SYSTEM', img)
    
    # Check for exit
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

# Cleanup and show summary
print("\n" + "="*60)
print("SYSTEM SHUTDOWN")
print("="*60)
print(f"\nTotal Access Attempts Logged: {len(access_log)}")
print("\nRecent Activity:")
for entry in access_log[-10:]:  # Show last 10 entries
    print(entry)
print("\n" + "="*60)

cam.release()
cv2.destroyAllWindows()