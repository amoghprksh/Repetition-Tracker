import cv2
import time
import numpy as np
import PoseModule as pm

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = pm.poseDetector()

count = 0
direction = 0

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # Extract landmarks for left arm
        left_shoulder = lmList[11]
        left_elbow = lmList[13]
        left_wrist = lmList[15]
        # Calculate angle between the elbow and shoulder
        angle = pm.calculate_angle(left_shoulder, left_elbow, left_wrist)

        # Check for correct form
        if angle > 160:
            direction = 1
            if count % 10 == 0:
                print("Correct form detected")
        elif angle < 30:
            direction = 0

        # Count bicep curls
        if direction == 1:
            if angle < 90:
                count += 0.5

        # Draw bicep curl count
        cv2.putText(img, f'Count: {count}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
