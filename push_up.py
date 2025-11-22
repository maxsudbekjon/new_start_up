# push_up_counter_drf.py

import cv2
import mediapipe as mp
import numpy as np
import time
import os
import django
from datetime import date
import sys
from task.models import  Do
from django.contrib.auth import get_user_model
from task.models.complete_task import CompleteTask
# 🧩 Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()



# 📱 Foydalanuvchini olish
def get_current_user():
    phone_number = '903149126'  # test user raqami
    print("🧑 Telefon raqam orqali qidirilmoqda:", phone_number)
    User = get_user_model()
    try:
        user = User.objects.get(phone_number=phone_number)
        return user
    except User.DoesNotExist:
        raise Exception(f"🚫 Foydalanuvchi topilmadi: phone_number='{phone_number}'")

# ✅ Bazaga saqlash
def save_to_db(user, do_title, count):
    do_obj, _ = Do.objects.get_or_create(title=do_title)
    today = date.today()
    task, created = CompleteTask.objects.get_or_create(
        user=user,
        do=do_obj,
        date=today,
        defaults={'count': count}
    )
    if not created:
        task.count += count
        task.save()

    print(f"✅ Bazaga saqlandi: {user.phone_number} — {do_title} — {task.count} ta")

# 🧍 To‘liq ko‘rinish tekshiruvi
def is_body_fully_visible(landmarks, shape, mp_pose):
    h, w = shape[:2]
    required = [
        "LEFT_SHOULDER", "LEFT_ELBOW", "LEFT_WRIST",
        "RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"
    ]
    for name in required:
        pt = landmarks[mp_pose.PoseLandmark[name].value]
        if pt.visibility < 0.7:
            return False
        if not (0 <= pt.x * w <= w and 0 <= pt.y * h <= h):
            return False
    return True

# 🔁 Push-Up sinf
class PushUpCounter:
    def __init__(self, max_count):
        self.max_count = max_count
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)
        self.cap = cv2.VideoCapture(0)
        self.counter = 0
        self.stage = None
        try:
            self.current_user = get_current_user()
        except Exception as e:
            print(f"❌ Foydalanuvchini olishda xatolik: {e}")
            self.current_user = None

    def calculate_angle(self, a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        return 360 - angle if angle > 180.0 else angle

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark
                h, w = frame.shape[:2]

                if not is_body_fully_visible(lm, (h, w), self.mp_pose):
                    self.stage = None
                    continue

                shoulder = [lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w,
                            lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
                elbow = [lm[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x * w,
                         lm[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y * h]
                wrist = [lm[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x * w,
                         lm[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y * h]

                angle = self.calculate_angle(shoulder, elbow, wrist)

                # Push-Up logika
                if angle < 90 and self.stage != 'down':
                    self.stage = 'down'
                elif angle > 160 and self.stage == 'down':
                    self.stage = 'up'
                    self.counter += 1
                    print(f"🔢 COUNT: {self.counter}", flush=True)
                    if self.current_user:
                        save_to_db(self.current_user, "Push-Up", 1)

                # 🖼️ Vizual
                cv2.putText(image, f"Push-Up: {self.counter}", (30, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3)
                cv2.putText(image, f"Burchak: {int(angle)}°", (30, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
                cv2.putText(image, f"Holat: {self.stage}", (30, 140),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)

                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            else:
                self.stage = None
                cv2.putText(image, f"Push-Up: {self.counter}", (30, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3)

            cv2.imshow("Push-Up Counter", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
        print(f"🏁 END_COUNT: {self.counter}", flush=True)

# 🧪 Ishga tushirish
if __name__ == "__main__":
    max_count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    counter = PushUpCounter(max_count)
    counter.run()