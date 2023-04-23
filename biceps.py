import cv2
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0

while True:
    success, img = cap.read()
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        # detect left and right arms
        left_arm_angle = detector.findAngle(img, 11, 13, 15)
        right_arm_angle = detector.findAngle(img, 12, 14, 16)
        # check if left arm is in bicep curl position
        if left_arm_angle > 160:
            if direction == 0:
                count += 1
                direction = 1
        # check if left arm is back to original position
        if left_arm_angle < 40:
            if direction == 1:
                direction = 0
        # check if right arm is in bicep curl position
        if right_arm_angle > 160:
            if direction == 0:
                count += 1
                direction = 1
        # check if right arm is back to original position
        if right_arm_angle < 40:
            if direction == 1:
                direction = 0

        # draw counts on image
        cv2.putText(img, f'Count: {count}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('Bicep Curls Counter', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()