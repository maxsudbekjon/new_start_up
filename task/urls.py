from task.views.complate_view import TaskCreateAPIView
from django.urls import path

urlpatterns = [
    path('task-create/', view=TaskCreateAPIView.as_view()),
]