# squat_counter_thread.py
import cv2
import mediapipe as mp
import numpy as np
import math
import os
import django
from datetime import date
import threading
from task.models import CompletedTask, Do
from django.contrib.auth import get_user_model

# Django sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

class SquatCounterThread(threading.Thread):
    def __init__(self, user_phone, task_title="Squat", count_limit=5):
        super().__init__()
        self.user_phone = user_phone
        self.task_title = task_title
        self.count_limit = count_limit
        self.counter = 0
        self.stage = None
        self.stopped = False

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

    def get_current_user(self):
        User = get_user_model()
        return User.objects.get(phone_number=self.user_phone)

    def save_to_db(self, user):
        do_object, _ = Do.objects.get_or_create(title=self.task_title)
        today = date.today()
        completed_task, created = CompletedTask.objects.get_or_create(
            user=user, do=do_object, date=today,
            defaults={'count': 1}
        )
        if not created:
            completed_task.count += 1
            completed_task.save()

    def calculate_angle(self, a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        radians = np.arccos(np.clip(np.dot(a - b, c - b) /
                    (np.linalg.norm(a - b) * np.linalg.norm(c - b)), -1.0, 1.0))
        return np.degrees(radians)

    def is_body_fully_visible(self, landmarks, shape):
        h, w = shape[:2]
        required = [
            "LEFT_HIP", "LEFT_KNEE", "LEFT_ANKLE",
            "RIGHT_HIP", "RIGHT_KNEE", "RIGHT_ANKLE"
        ]
        for name in required:
            pt = landmarks[self.mp_pose.PoseLandmark[name].value]
            if pt.visibility < 0.7:
                return False
            if not (0 <= pt.x * w <= w and 0 <= pt.y * h <= h):
                return False
        return True

    def run(self):
        print("▶️ SquatCounterThread boshlanmoqda...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Kamera ochilmadi")
            return
        print("✅ Kamera ochildi")

        try:
            user =1
        except Exception as e:
            print(f"❌ Foydalanuvchi topilmadi: {e}")
            return

        while cap.isOpened() and not self.stopped:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                shape = frame.shape
                landmarks = results.pose_landmarks.landmark

                if not self.is_body_fully_visible(landmarks, shape):
                    self.stage = None
                    continue

                l_hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x * shape[1],
                         landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y * shape[0]]
                l_knee = [landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x * shape[1],
                          landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y * shape[0]]
                l_ankle = [landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x * shape[1],
                           landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y * shape[0]]

                r_hip = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x * shape[1],
                         landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y * shape[0]]
                r_knee = [landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x * shape[1],
                          landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y * shape[0]]
                r_ankle = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * shape[1],
                           landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * shape[0]]

                l_angle = self.calculate_angle(l_hip, l_knee, l_ankle)
                r_angle = self.calculate_angle(r_hip, r_knee, r_ankle)

                if l_angle <= 120 and r_angle <= 120:
                    if self.stage != "down":
                        self.stage = "down"

                elif l_angle >= 160 and r_angle >= 160:
                    if self.stage == "down":
                        self.stage = "up"
                        self.counter += 1
                        print(f"🧮 COUNT: {self.counter}", flush=True)
                        self.save_to_db(user)

                cv2.putText(image, f"Squat: {self.counter}", (30, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3)

            cv2.imshow("Squat Counter", image)
            if cv2.waitKey(1) & 0xFF == ord("q") or self.counter >= self.count_limit:
                break

        cap.release()
        cv2.destroyAllWindows()
        print("⛔ SquatCounterThread tugadi.")
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("❗ Foydalanuvchi raqami va count kerak: python3 squat_counter_thread.py <phone_number> <count>")
        sys.exit(1)

    phone_number = sys.argv[1]
    try:
        count_limit = int(sys.argv[2])
    except ValueError:
        print("❗ Count butun son bo‘lishi kerak")
        sys.exit(1)

    thread = SquatCounterThread(user_phone=phone_number, count_limit=count_limit)
    thread.start()
    thread.join()