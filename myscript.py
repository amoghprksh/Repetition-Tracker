import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize Mediapipe pose detection
pose_detection = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize video capture
cap = cv2.VideoCapture(0)

reps = 0
max_reps = 0
last_pose = None

while True:
    success, image = cap.read()
    if not success:
        break
    
    # Convert the image to RGB format and process with Mediapipe
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose_detection.process(image)
    
    # Draw pose landmarks on the image
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Calculate the angle between the hips, knees, and ankles to detect deadlifts
        left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        left_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        left_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
        right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
        right_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
        right_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
        
        left_angle = 50#calculate_angle(left_hip, left_knee, left_ankle)
        right_angle = 100#calculate_angle(right_hip, right_knee, right_ankle)
        avg_angle = (left_angle + right_angle) / 2
        
        if last_pose == "down" and avg_angle > 90:
            reps += 1
            if reps > max_reps:
                max_reps = reps
            last_pose = "up"
        elif last_pose == "up" and avg_angle < 70:
            last_pose = "down"
        
        cv2.putText(image, f"Repetitions: {reps}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(image, f"Max Repetitions: {max_reps}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
    cv2.imshow("Deadlift Repetition Tracker", image)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
pose_detection.close()

#def calculate_angle(a, b, c):
    # Calculate the angle between three points using the law of cosines
#    angle = np.arccos(np.square(b.x-a.x) + np.square(b.y-a.y) + np.square(b.z-a.z) + np.square(c.x-b.x) + np.square(c.y-b.y) + np.square(c.z-b.z) - np.square(a.x-c.x) - np.square(a.y-c.y) - np.square(a.z-c.z)) / (2 * np.sqrt(np.square(b.x-a.x) + np.square(b.y-a.y) + np.square(b.z-a.z))