'''
FINAL Stable Face Recognition System
Once verified, stays verified until face leaves
'''

import cv2
import numpy as np
from datetime import datetime

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

# SECURITY SETTINGS
CONFIDENCE_THRESHOLD = 60
CONSECUTIVE_FRAMES_REQUIRED = 5
DOOR_UNLOCK_DURATION = 5  # Door stays unlocked for 5 seconds

# User database
names = ['None', 'Sarthak', 'Person2', 'Person3', 'Person4', 'Person5', 'Person6', 'Person7', 'Person8', 'Person9', 'Person10']

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

print("\n" + "="*70)
print("FINAL STABLE ACCESS CONTROL SYSTEM")
print("="*70)
print(f"Confidence Threshold: {CONFIDENCE_THRESHOLD}")
print(f"Frames Required for Verification: {CONSECUTIVE_FRAMES_REQUIRED}")
print(f"Door Unlock Duration: {DOOR_UNLOCK_DURATION} seconds")
print("="*70)
print("\nColor Guide:")
print("  GREEN   = Access Granted (Door Unlocked)")
print("  YELLOW  = Verifying Identity")
print("  RED     = Access Denied")
print("\nSystem Status: ACTIVE | Press ESC to exit\n")

# State tracking
current_verified_person = None  # Currently verified person
verification_count = {}  # Count frames for verification
door_unlock_time = None  # When door was unlocked
door_is_unlocked = False  # Door state
access_log = []
frame_count = 0
no_face_frames = 0  # Count frames without face

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
    
    # Check if door unlock has expired
    if door_is_unlocked and door_unlock_time:
        time_since_unlock = (current_time - door_unlock_time).total_seconds()
        if time_since_unlock >= DOOR_UNLOCK_DURATION:
            door_is_unlocked = False
            print(f"[{current_time.strftime('%H:%M:%S')}] Door locked (timeout)")
    
    # No face detected
    if len(faces) == 0:
        no_face_frames += 1
        
        # If no face for 30 frames (about 1 second), reset verification
        if no_face_frames > 30:
            if current_verified_person:
                print(f"[{current_time.strftime('%H:%M:%S')}] {current_verified_person} left")
            current_verified_person = None
            verification_count = {}
        
        # Display status based on door state
        if door_is_unlocked:
            remaining = DOOR_UNLOCK_DURATION - int((current_time - door_unlock_time).total_seconds())
            cv2.putText(img, f"DOOR UNLOCKED - {remaining}s remaining", (20, 50), 
                        font, 1, (0, 255, 0), 2)
        else:
            cv2.putText(img, "READY - Waiting for face...", (20, 50), 
                        font, 1, (255, 255, 255), 2)
    else:
        no_face_frames = 0  # Reset no-face counter
        
        for (x, y, w, h) in faces:
            id_result, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            
            match_percentage = round(100 - confidence)
            confidence_text = f"Conf: {round(confidence)} | Match: {match_percentage}%"
            
            if confidence < CONFIDENCE_THRESHOLD:
                # Valid recognition
                if id_result < len(names):
                    person_name = names[id_result]
                else:
                    person_name = f"User{id_result}"
                
                # Check if this person is already verified
                if current_verified_person == person_name:
                    # ALREADY VERIFIED - STAY GREEN
                    box_color = (0, 255, 0)
                    status = f"VERIFIED - {person_name}"
                    status_color = (0, 255, 0)
                    
                    # Keep door unlocked
                    if not door_is_unlocked:
                        door_is_unlocked = True
                        door_unlock_time = current_time
                        log_entry = f"[{current_time.strftime('%H:%M:%S')}] DOOR UNLOCKED - {person_name}"
                        access_log.append(log_entry)
                        print(log_entry)
                        # TRIGGER DOOR UNLOCK HERE
                    else:
                        # Extend unlock time while face is present
                        door_unlock_time = current_time
                
                else:
                    # NEW PERSON - Need to verify
                    if person_name not in verification_count:
                        verification_count[person_name] = 1
                    else:
                        verification_count[person_name] += 1
                    
                    frames_verified = verification_count[person_name]
                    
                    if frames_verified >= CONSECUTIVE_FRAMES_REQUIRED:
                        # VERIFICATION COMPLETE
                        current_verified_person = person_name
                        verification_count = {person_name: frames_verified}  # Keep only current
                        
                        box_color = (0, 255, 0)
                        status = f"ACCESS GRANTED - {person_name}"
                        status_color = (0, 255, 0)
                        
                        # Unlock door
                        door_is_unlocked = True
                        door_unlock_time = current_time
                        
                        log_entry = f"[{current_time.strftime('%H:%M:%S')}] ACCESS GRANTED - {person_name}"
                        access_log.append(log_entry)
                        print(log_entry)
                        
                        # TRIGGER DOOR UNLOCK HERE
                        # Example: GPIO.output(LOCK_PIN, GPIO.HIGH)
                        
                    else:
                        # STILL VERIFYING
                        box_color = (0, 255, 255)
                        status = f"VERIFYING: {person_name} ({frames_verified}/{CONSECUTIVE_FRAMES_REQUIRED})"
                        status_color = (0, 255, 255)
            else:
                # NOT RECOGNIZED
                person_name = "UNKNOWN"
                box_color = (0, 0, 255)
                status = "ACCESS DENIED - Unknown Person"
                status_color = (0, 0, 255)
                
                # Reset verification
                current_verified_person = None
                verification_count = {}
                
                # Log denial
                if frame_count % 30 == 0:
                    log_entry = f"[{current_time.strftime('%H:%M:%S')}] ACCESS DENIED - Unknown"
                    if len(access_log) == 0 or "DENIED" not in access_log[-1]:
                        access_log.append(log_entry)
                        print(log_entry)
            
            # Draw face box
            cv2.rectangle(img, (x, y), (x+w, y+h), box_color, 4)
            
            # Display name
            cv2.putText(img, person_name, (x+5, y-50), font, 1.2, (255, 255, 255), 3)
            
            # Display confidence
            cv2.putText(img, confidence_text, (x+5, y-15), 
                        font, 0.5, (255, 255, 255), 1)
            
            # Main status at top
            cv2.putText(img, status, (20, 50), font, 1, status_color, 3)
            
            # Door status
            if door_is_unlocked:
                remaining = DOOR_UNLOCK_DURATION - int((current_time - door_unlock_time).total_seconds())
                door_status = f"DOOR: UNLOCKED ({remaining}s)"
                door_color = (0, 255, 0)
            else:
                door_status = "DOOR: LOCKED"
                door_color = (0, 0, 255)
            
            cv2.putText(img, door_status, (20, 100), font, 0.8, door_color, 2)
            
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
print("\nAccess Log:")
for entry in access_log:
    print(entry)
print("="*70)

cam.release()
cv2.destroyAllWindows()