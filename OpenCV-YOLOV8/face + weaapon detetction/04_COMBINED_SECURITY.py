import cv2
import numpy as np
from datetime import datetime
from ultralytics import YOLO

# --- 1. FACE RECOGNITION SETUP ---
RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()
RECOGNIZER.read('trainer/trainer.yml')
FACE_CASCADE = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
FONT = cv2.FONT_HERSHEY_SIMPLEX

# Security Settings for Face Recognition
CONFIDENCE_THRESHOLD = 60      # Max score for a 'match' (lower is better, 60 is balanced)
CONSECUTIVE_FRAMES_REQUIRED = 5 # Frames needed to confirm identity

# User Database (Ensure this matches your training IDs)
NAMES = ['None', 'Sarthak', 'Person2', 'Person3', 'Person4', 'Person5', 'Person6', 'Person7', 'Person8', 'Person9', 'Person10']

# Tracking Variables
consecutive_recognitions = {}
last_access_time = {}
ACCESS_COOLDOWN = 5 # seconds

# --- 2. WEAPON DETECTION SETUP ---
# CRITICAL: This file MUST be in the same folder as this script
WEAPON_MODEL = YOLO('best.pt')

# --- 3. CAMERA SETUP ---
CAM = cv2.VideoCapture(0)
CAM.set(3, 640)
CAM.set(4, 480)
MIN_W = 0.1 * CAM.get(3)
MIN_H = 0.1 * CAM.get(4)

print("="*70)
print("INTEGRATED FACE + WEAPON SECURITY SYSTEM - ACTIVE")
print("="*70)

while True:
    ret, img = CAM.read()
    if not ret:
        print("[ERROR] Camera error")
        break

    img = cv2.flip(img, 1)
    current_time = datetime.now()
    
    # --- A. RUN WEAPON DETECTION (YOLOv8) ---
    weapon_results = WEAPON_MODEL(img, verbose=False)[0] # Run YOLO model
    weapon_detected = False
    
    # Check YOLO results for any detected objects
    for box in weapon_results.boxes:
        if box.conf[0].item() > 0.5: # Only consider detections with > 50% confidence
            weapon_detected = True
            
            # Draw bounding box for weapon
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2) # PURPLE box for weapon
            cv2.putText(img, f"WEAPON: {box.conf[0].item():.2f}", (x1, y1 - 10), FONT, 0.6, (255, 0, 255), 2)
            break # Stop checking after first weapon found

    # --- B. RUN FACE RECOGNITION (OpenCV) ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(MIN_W), int(MIN_H))
    )
    
    # Default decision if no face is found
    final_status = "READY - Waiting for face..."
    status_color = (255, 255, 255) 

    if len(faces) == 0:
        consecutive_recognitions = {}

    for (x, y, w, h) in faces:
        id_result, confidence = RECOGNIZER.predict(gray[y:y+h, x:x+w])
        match_percentage = round(100 - confidence)
        
        person_name = "UNKNOWN"
        box_color = (0, 0, 255) # RED
        
        # 1. Determine Identity
        if confidence < CONFIDENCE_THRESHOLD:
            if id_result < len(NAMES):
                person_name = NAMES[id_result]
            else:
                person_name = f"User{id_result} (Unlisted)"
        
        # 2. Determine Final Access (Face + Weapon)
        if person_name != "UNKNOWN":
            
            # Access Denied due to Weapon
            if weapon_detected:
                final_status = f"ACCESS DENIED (ARMED - {person_name})"
                status_color = (128, 0, 128) # DARK PURPLE
                box_color = (128, 0, 128)
                consecutive_recognitions = {} # Reset to require re-verification
            
            # Check for Access Grant (No Weapon)
            else:
                # Track consecutive frames
                consecutive_recognitions[person_name] = consecutive_recognitions.get(person_name, 0) + 1
                frames_recognized = consecutive_recognitions[person_name]

                if frames_recognized >= CONSECUTIVE_FRAMES_REQUIRED:
                    # Check cooldown
                    time_since = (current_time - last_access_time.get(person_name, datetime.min)).total_seconds()
                    
                    if time_since >= ACCESS_COOLDOWN:
                        # ACCESS GRANTED
                        final_status = f"ACCESS GRANTED - {person_name}"
                        status_color = (0, 255, 0) # GREEN
                        box_color = (0, 255, 0)
                        last_access_time[person_name] = current_time
                        print(f"[{current_time.strftime('%H:%M:%S')}] {final_status}")
                        # HERE: ADD DOOR UNLOCK LOGIC
                    else:
                        # Cooldown
                        remaining = ACCESS_COOLDOWN - int(time_since)
                        final_status = f"COOLDOWN - Wait {remaining}s"
                        status_color = (0, 165, 255) # ORANGE
                        box_color = (0, 165, 255)
                else:
                    # Verifying
                    final_status = f"VERIFYING: {person_name} ({frames_recognized}/{CONSECUTIVE_FRAMES_REQUIRED})"
                    status_color = (0, 255, 255) # YELLOW
                    box_color = (0, 255, 255)

        else: # UNKNOWN person
            final_status = "ACCESS DENIED - UNKNOWN PERSON"
            status_color = (0, 0, 255) # RED
            consecutive_recognitions = {}
            # Log denial
            if weapon_detected:
                print(f"[{current_time.strftime('%H:%M:%S')}] ACCESS DENIED - UNKNOWN ARMED")
            else:
                print(f"[{current_time.strftime('%H:%M:%S')}] ACCESS DENIED - UNKNOWN")

        # Draw Face box and info
        cv2.rectangle(img, (x, y), (x+w, y+h), box_color, 4)
        cv2.putText(img, person_name, (x+5, y-50), FONT, 1.2, (255, 255, 255), 3)
        cv2.putText(img, f"Match: {match_percentage}%", (x+5, y-15), FONT, 0.5, (255, 255, 255), 1)

    # Display overall status at the top
    cv2.putText(img, final_status, (20, 50), FONT, 1, status_color, 3)
    cv2.imshow('INTEGRATED HIGH SECURITY', img)

    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

CAM.release()
cv2.destroyAllWindows()
print("System Shutdown.")