import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

counter = 0
stage = None  # Holat: "down" yoki "up"

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

print("📹 Kamera ishga tushdi. 'q' tugmasi bilan chiqishingiz mumkin.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)
    image = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    h, w = frame.shape[:2]

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # O'ng yelka, tirsak va bilak koordinatalari
        lm = results.pose_landmarks.landmark
        shoulder = [lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * w,
                    lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
        elbow = [lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * w,
                 lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * h]
        wrist = [lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * w,
                 lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * h]

        angle = calculate_angle(shoulder, elbow, wrist)

        # Push-Up logika
        if angle < 90 and stage != 'down':
            stage = 'down'
        elif angle > 160 and stage == 'down':
            stage = 'up'
            counter += 1

        cv2.putText(image, f"Odam aniqlandi", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        cv2.putText(image, f"Push-Up: {counter}", (30, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
        cv2.putText(image, f"Holat: {stage}", (30, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)

    else:
        cv2.putText(image, f"Odam yo'q", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    cv2.imshow("Camera - Odam va Mashq Counter", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
