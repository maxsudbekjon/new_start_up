from task.views.complate_view import ComplateTaskListAPIView, ComplateTaskCreateAPIView
from django.urls import path
from task.views.taskserializer import TaskListAPIView, ProgramCreatAPIView, TaskCreateAPIView, DoCreatAPIView

urlpatterns = [
    path('Complate_task-list/', view=ComplateTaskListAPIView.as_view()),
    path('Complate_task-create/', view=ComplateTaskCreateAPIView.as_view()),

    path("Task-list/", view=TaskListAPIView.as_view()),
    path("Task-create/", view=TaskCreateAPIView.as_view()),

    path("Program-create/", view=ProgramCreatAPIView.as_view()),

    path("Do-create/", view=DoCreatAPIView.as_view()),
]