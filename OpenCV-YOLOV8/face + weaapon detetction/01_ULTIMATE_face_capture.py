'''
ULTIMATE Face Capture - 300 Images for Maximum Accuracy
'''

import cv2
import os
import time

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

print("\n" + "="*60)
print("ULTIMATE FACE CAPTURE SYSTEM - 300 IMAGES")
print("="*60)

face_id = input('\nEnter User ID (number): ')
user_name = input('Enter Name: ')

print("\n" + "="*60)
print("CAPTURE INSTRUCTIONS:")
print("="*60)
print("This will capture 300 HIGH QUALITY images")
print("1. Good lighting on your face")
print("2. Stay arm's length from camera")
print("3. During capture, SLOWLY:")
print("   - Turn head left to right")
print("   - Look up and down")
print("   - Try different expressions")
print("   - Slight smile, neutral, serious")
print("\nPress SPACE to start, ESC to cancel")
print("="*60)

cv2.namedWindow('ULTIMATE Face Capture')

# Wait for ready
while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1)
    
    cv2.putText(img, "Position your face in frame", (50, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, "Press SPACE when ready", (50, 150), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
    
    cv2.imshow('ULTIMATE Face Capture', img)
    
    key = cv2.waitKey(1) & 0xff
    if key == 32:
        break
    elif key == 27:
        print("\nCancelled")
        cam.release()
        cv2.destroyAllWindows()
        exit(0)

print("\n[INFO] Starting in 3 seconds...")
for i in range(3, 0, -1):
    print(f"[INFO] {i}...")
    time.sleep(1)

print("[INFO] CAPTURING NOW!\n")

TARGET_IMAGES = 300
captured = 0
last_capture_time = time.time()
MIN_INTERVAL = 0.1  # 100ms between captures

while captured < TARGET_IMAGES:
    ret, img = cam.read()
    
    if not ret:
        break
    
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(80, 80)
    )
    
    current_time = time.time()
    
    # Progress bar
    progress_width = 500
    progress = int((captured / TARGET_IMAGES) * progress_width)
    
    cv2.rectangle(img, (70, 420), (70 + progress_width, 450), (50, 50, 50), -1)
    cv2.rectangle(img, (70, 420), (70 + progress, 450), (0, 255, 0), -1)
    cv2.putText(img, f"{captured}/{TARGET_IMAGES} images", (70, 410), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
            
            if current_time - last_capture_time >= MIN_INTERVAL:
                filename = f"dataset/User.{face_id}.{captured + 1}.jpg"
                cv2.imwrite(filename, gray[y:y+h, x:x+w])
                captured += 1
                last_capture_time = current_time
                
                if captured % 20 == 0:
                    print(f"[INFO] Progress: {captured}/{TARGET_IMAGES}")
                
                # Flash effect
                cv2.rectangle(img, (0, 0), (640, 480), (255, 255, 255), 10)
            
            # Instructions based on progress
            if captured < 50:
                instruction = "Look STRAIGHT"
            elif captured < 100:
                instruction = "Turn head LEFT slowly"
            elif captured < 150:
                instruction = "Turn head RIGHT slowly"
            elif captured < 200:
                instruction = "Look UP slightly"
            elif captured < 250:
                instruction = "Look DOWN slightly"
            elif captured < 280:
                instruction = "SMILE"
            else:
                instruction = "Almost done! Neutral face"
            
            cv2.putText(img, instruction, (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            break
    else:
        cv2.putText(img, "NO FACE - Position yourself!", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.imshow('ULTIMATE Face Capture', img)
    
    key = cv2.waitKey(1) & 0xff
    if key == 27:
        print("\n[INFO] Stopped by user")
        break

print("\n" + "="*60)
print(f"[SUCCESS] Captured {captured} images for {user_name} (ID: {face_id})")
print("="*60)

cam.release()
cv2.destroyAllWindows()