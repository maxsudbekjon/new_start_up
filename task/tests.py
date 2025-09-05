from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from .models import Task, Do, Program

User = get_user_model()


class AddTaskAPIViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            age=9,  # yoshini 10 dan kichik qilib qo‘ydik,
            phone="+998889272703",
        )
        self.client.force_authenticate(user=self.user)
        self.url = "/task/add_task/"  # sizning endpointingiz shu bo‘lishi kerak

    def test_age_filter_rejects_invalid_count(self):
        """Agar yosh <= 10 bo‘lsa va count > 5 bo‘lsa xato qaytishi kerak"""
        response = self.client.post(self.url, {"title": "Test Task", "count": 7})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_age_filter_accepts_valid_count(self):
        """Agar yosh <= 10 bo‘lsa va count <= 5 bo‘lsa task yaratilishi kerak"""
        response = self.client.post(self.url, {"title": "Valid Task", "count": 5})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_streak_increases_after_30_days(self):
        """30 kun davomida task qoldirmasdan bajarganda count oshishi kerak"""
        self.user.age = 25  # katta yosh bo‘lsa limit balandroq
        self.user.save()

        for i in range(30):
            response = self.client.post(self.url, {"title": f"Day {i+1}", "count": 10})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Endi foydalanuvchining oxirgi task counti 13 ga oshganini tekshirish kerak
        last_task = Task.objects.last()
        self.assertEqual(last_task.count, 13)

    def test_streak_resets_if_task_skipped(self):
        """Bitta kun task qilinmasa streak nolga tushib ketishi kerak"""
        self.user.age = 25
        self.user.save()

        # 10 kun task qilamiz
        for i in range(10):
            self.client.post(self.url, {"title": f"Day {i+1}", "count": 10})

        # Bitta kunni tashlab yuborgan deb hisoblaymiz:
        do = Do.objects.create(title="Fake Old Task")
        program = Program.objects.create(title="asasas")
        Task.objects.create(user=self.user, title=do, program=program, count=10,
                            duration="45:45", is_complete=True)

        response = self.client.post(self.url, {"title": "After Skip", "count": 10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        last_task = Task.objects.last()
        self.assertEqual(last_task.count, 10)  # count streak reset bo‘ldi
