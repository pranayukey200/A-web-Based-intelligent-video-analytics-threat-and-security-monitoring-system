'''
Professional Face Dataset Capture - High Accuracy Version
Captures 100+ images with proper quality control
'''

import cv2
import os
import time

# Initialize camera
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Width
cam.set(4, 480)  # Height

# Load face detector
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Get user information
print("\n" + "="*50)
print("PROFESSIONAL FACE CAPTURE SYSTEM")
print("="*50)

face_id = input('\nEnter User ID (number only): ')
user_name = input('Enter User Name: ')

print("\n" + "="*50)
print("CAPTURE INSTRUCTIONS:")
print("="*50)
print("1. Look directly at the camera")
print("2. Ensure good lighting on your face")
print("3. Stay at arm's length from camera")
print("4. System will capture 100 images")
print("5. Move your head SLIGHTLY during capture:")
print("   - Look left, then center, then right")
print("   - Look up slightly, then center, then down")
print("   - Try different expressions (smile, neutral, serious)")
print("\nPress any key when ready...")
print("="*50)

# Wait for user to be ready
cv2.namedWindow('Face Capture System')
while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1)
    
    # Display instructions on screen
    cv2.putText(img, "Position your face in the frame", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, "Press SPACE when ready to start", (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow('Face Capture System', img)
    
    key = cv2.waitKey(1) & 0xff
    if key == 32:  # Space bar
        break
    elif key == 27:  # ESC
        print("\n[INFO] Capture cancelled by user")
        cam.release()
        cv2.destroyAllWindows()
        exit(0)

print("\n[INFO] Starting capture in 3 seconds...")
time.sleep(1)
print("[INFO] 3...")
time.sleep(1)
print("[INFO] 2...")
time.sleep(1)
print("[INFO] 1...")
time.sleep(1)
print("[INFO] CAPTURING NOW!\n")

count = 0
captured = 0
no_face_count = 0
last_capture_time = time.time()
MIN_CAPTURE_INTERVAL = 0.15  # Minimum 150ms between captures (prevents freezing)

while captured < 100:
    ret, img = cam.read()
    
    if not ret:
        print("[ERROR] Failed to read from camera")
        break
    
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(100, 100)  # Minimum face size
    )
    
    current_time = time.time()
    
    # Display progress
    progress_bar_width = 400
    progress = int((captured / 100) * progress_bar_width)
    
    cv2.rectangle(img, (10, 400), (10 + progress_bar_width, 430), (50, 50, 50), -1)
    cv2.rectangle(img, (10, 400), (10 + progress, 430), (0, 255, 0), -1)
    cv2.putText(img, f"Progress: {captured}/100 images", (10, 390), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    if len(faces) == 0:
        no_face_count += 1
        cv2.putText(img, "NO FACE DETECTED!", (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, "Position your face in frame", (10, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        no_face_count = 0
        
        for (x, y, w, h) in faces:
            # Only capture one face at a time (the first detected)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
            
            # Check quality - face should be large enough
            face_area = w * h
            frame_area = img.shape[0] * img.shape[1]
            face_ratio = face_area / frame_area
            
            if face_ratio < 0.05:  # Face too small
                cv2.putText(img, "MOVE CLOSER!", (x, y-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            elif face_ratio > 0.4:  # Face too large
                cv2.putText(img, "MOVE BACK!", (x, y-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                # Good distance - capture if enough time has passed
                if current_time - last_capture_time >= MIN_CAPTURE_INTERVAL:
                    # Save image
                    filename = f"dataset/User.{face_id}.{captured + 1}.jpg"
                    cv2.imwrite(filename, gray[y:y+h, x:x+w])
                    captured += 1
                    last_capture_time = current_time
                    
                    print(f"[INFO] Captured: {captured}/100")
                    
                    # Visual feedback
                    cv2.rectangle(img, (0, 0), (img.shape[1], img.shape[0]), (0, 255, 0), 5)
                
                cv2.putText(img, "GOOD! Hold position", (x, y-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Instructions
            if captured < 30:
                instruction = "Look straight ahead"
            elif captured < 50:
                instruction = "Turn head slightly LEFT"
            elif captured < 70:
                instruction = "Turn head slightly RIGHT"
            elif captured < 85:
                instruction = "Look up slightly"
            elif captured < 95:
                instruction = "Look down slightly"
            else:
                instruction = "Almost done! Stay still"
            
            cv2.putText(img, instruction, (10, 350), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
            
            break  # Only process first face
    
    cv2.imshow('Face Capture System', img)
    
    # Check for ESC key
    key = cv2.waitKey(1) & 0xff
    if key == 27:
        print("\n[INFO] Capture stopped by user")
        break
    
    count += 1

# Cleanup
print("\n" + "="*50)
print(f"[SUCCESS] Captured {captured} images for {user_name} (ID: {face_id})")
print("="*50)
print("[INFO] Exiting and cleaning up...")
cam.release()
cv2.destroyAllWindows()