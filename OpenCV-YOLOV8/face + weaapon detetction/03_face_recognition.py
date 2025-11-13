'''
Debug version - shows detailed error messages
'''

import cv2
import numpy as np
import os
import traceback

try:
    print("[DEBUG] Starting face recognition...")
    print("[DEBUG] Loading recognizer...")
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    print("[DEBUG] Reading trainer file...")
    recognizer.read('trainer/trainer.yml')
    
    print("[DEBUG] Loading cascade classifier...")
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    
    if faceCascade.empty():
        print("[ERROR] Failed to load cascade classifier!")
        exit(1)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    id = 0
    
    names = ['None', 'Sarthak', 'Person2', 'Person3', 'Person4', 'Person5']
    
    print("[DEBUG] Opening webcam...")
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
        print("[ERROR] Cannot open webcam!")
        exit(1)
    
    print("[DEBUG] Webcam opened successfully")
    cam.set(3, 640)
    cam.set(4, 480)
    
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    
    print("[INFO] Face recognition started. Press ESC to exit.")
    
    frame_count = 0
    while True:
        ret, img = cam.read()
        
        if not ret:
            print("[ERROR] Failed to read frame from webcam")
            break
        
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"[DEBUG] Processing frame {frame_count}")
        
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        
        for(x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            
            if (confidence < 100):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x+5, y+h-5), font, 1, (255, 255, 0), 1)
        
        cv2.imshow('camera', img)
        
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            print("[INFO] ESC pressed, exiting...")
            break
    
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(f"\n[ERROR] An error occurred:")
    print(f"[ERROR] {str(e)}")
    print("\n[ERROR] Full traceback:")
    traceback.print_exc()