'''
OPTIMIZED High Security Face Recognition
Balanced settings for real-world use
'''

import cv2
import numpy as np
from datetime import datetime

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

# OPTIMIZED SECURITY SETTINGS
CONFIDENCE_THRESHOLD = 60  # Balanced (was 45 - too strict)
CONSECUTIVE_FRAMES_REQUIRED = 5  # Need 5 frames for security
ACCESS_COOLDOWN = 2

# User database - ADD MORE NAMES IF YOU HAVE MORE USERS
names = ['None', 'Sarthak', 'Person2', 'Person3', 'Person4', 'Person5', 'Person6', 'Person7', 'Person8', 'Person9', 'Person10']

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

print("\n" + "="*70)
print("OPTIMIZED SECURE ACCESS CONTROL SYSTEM")
print("="*70)
print(f"Confidence Threshold: {CONFIDENCE_THRESHOLD} (Lower = Stricter)")
print(f"Required Recognition Frames: {CONSECUTIVE_FRAMES_REQUIRED}")
print(f"Access Cooldown: {ACCESS_COOLDOWN} seconds")
print("="*70)
print("\nColor Guide:")
print("  GREEN   = Access Granted")
print("  YELLOW  = Verifying Identity")
print("  ORANGE  = Cooldown Period")
print("  RED     = Access Denied")
print("\nSystem Status: ACTIVE | Press ESC to exit\n")

# Tracking
consecutive_recognitions = {}
last_access_time = {}
access_log = []
frame_count = 0

while True:
    ret, img = cam.read()
    
    if not ret:
        print("[ERROR] Camera error")
        break
    
    frame_count += 1
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )
    
    current_time = datetime.now()
    
    # Clear tracking if no faces
    if len(faces) == 0:
        consecutive_recognitions = {}
        # Display "Ready" status
        cv2.putText(img, "READY - Waiting for face...", (20, 50), 
                    font, 1, (255, 255, 255), 2)
    
    for (x, y, w, h) in faces:
        id_result, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        
        match_percentage = round(100 - confidence)
        
        # Show confidence value for debugging
        confidence_text = f"Conf: {round(confidence)} | Match: {match_percentage}%"
        
        if confidence < CONFIDENCE_THRESHOLD:
            # RECOGNIZED - FIX FOR INDEX ERROR
            if id_result < len(names):
                person_name = names[id_result]
            else:
                person_name = f"User{id_result}"
            
            # Count consecutive frames
            if person_name not in consecutive_recognitions:
                consecutive_recognitions[person_name] = 1
            else:
                consecutive_recognitions[person_name] += 1
            
            frames_recognized = consecutive_recognitions[person_name]
            
            if frames_recognized >= CONSECUTIVE_FRAMES_REQUIRED:
                # Check cooldown
                if person_name not in last_access_time:
                    last_access_time[person_name] = datetime.min
                
                time_since = (current_time - last_access_time[person_name]).total_seconds()
                
                if time_since >= ACCESS_COOLDOWN:
                    # ACCESS GRANTED
                    box_color = (0, 255, 0)
                    status = f"ACCESS GRANTED - {person_name}"
                    status_color = (0, 255, 0)
                    
                    log_entry = f"[{current_time.strftime('%H:%M:%S')}] ACCESS GRANTED - {person_name}"
                    
                    if len(access_log) == 0 or access_log[-1] != log_entry:
                        access_log.append(log_entry)
                        print(log_entry)
                    
                    last_access_time[person_name] = current_time
                    
                    # DOOR UNLOCK HERE
                    # Add your door unlock code
                    
                else:
                    # Cooldown
                    box_color = (0, 165, 255)
                    remaining = ACCESS_COOLDOWN - int(time_since)
                    status = f"COOLDOWN - Wait {remaining}s"
                    status_color = (0, 165, 255)
            else:
                # Verifying
                box_color = (0, 255, 255)
                status = f"VERIFYING: {person_name} ({frames_recognized}/{CONSECUTIVE_FRAMES_REQUIRED})"
                status_color = (0, 255, 255)
        else:
            # NOT RECOGNIZED
            person_name = "UNKNOWN"
            box_color = (0, 0, 255)
            status = "ACCESS DENIED - Unknown Person"
            status_color = (0, 0, 255)
            consecutive_recognitions = {}
            
            # Log denial (only once per sequence)
            if frame_count % 30 == 0:
                log_entry = f"[{current_time.strftime('%H:%M:%S')}] ACCESS DENIED - Unknown"
                if len(access_log) == 0 or "DENIED" not in access_log[-1]:
                    access_log.append(log_entry)
                    print(log_entry)
        
        # Draw face box
        cv2.rectangle(img, (x, y), (x+w, y+h), box_color, 4)
        
        # Display name (larger font)
        cv2.putText(img, person_name, (x+5, y-50), font, 1.2, (255, 255, 255), 3)
        
        # Display confidence details
        cv2.putText(img, confidence_text, (x+5, y-15), 
                    font, 0.5, (255, 255, 255), 1)
        
        # Main status at top
        cv2.putText(img, status, (20, 50), font, 1, status_color, 3)
        
        # Security info at bottom
        security_info = f"Security: HIGH | Threshold: {CONFIDENCE_THRESHOLD} | Frames: {CONSECUTIVE_FRAMES_REQUIRED}"
        cv2.putText(img, security_info, (10, 470), font, 0.5, (200, 200, 200), 1)
    
    cv2.imshow('SECURE ACCESS CONTROL', img)
    
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

# Summary
print("\n" + "="*70)
print("SYSTEM SHUTDOWN")
print("="*70)
print(f"Total Events Logged: {len(access_log)}")
print("\nRecent Activity:")
for entry in access_log[-15:]:
    print(entry)
print("="*70)

cam.release()
cv2.destroyAllWindows()