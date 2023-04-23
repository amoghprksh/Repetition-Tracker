import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()

deadlift_count = 0
deadlift_started = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)
    
    if lmList != None:
        angle = detector.findAngle(img, 11, 13, 15)
        
        if angle > 160:
            if not deadlift_started:
                deadlift_started = True
        elif angle < 100:
            if deadlift_started:
                deadlift_started = False
                deadlift_count += 1
                print("Deadlift Count:", deadlift_count)

        cv2.putText(img, str(deadlift_count), (50, 100), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 10)
    
    cv2.imshow('Deadlifts Counter', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()