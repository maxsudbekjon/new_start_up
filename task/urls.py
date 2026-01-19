from django.urls import path
from task.views.complate_view import  MonthlyCompleteTaskAPIView, TodayCompletedTasksCountView, UserTaskHistoryView, WeeklyCompleteTaskAPIView, YearlyCompleteTaskAPIView
from task.views.do_view import  AddDoAPIView, ListDoAPIView
from task.views.program_view import  GetTaskProgram, ListProgramAPIView
from task.views.task_view import AddTaskAPIView, CompleteTaskView, ListTaskAPIView, UpdateTaskAPIView, DeleteTaskAPIView





#   TASK
urlpatterns = [
    path('add_task/', AddTaskAPIView.as_view()),
    path("get/do/program<str:program>",GetTaskProgram.as_view()),
    path('get_task_list/', ListTaskAPIView.as_view()),
    path('update_task/<int:pk>/', UpdateTaskAPIView.as_view()),
    path('delete_task/<int:pk>/', DeleteTaskAPIView.as_view()),
    path("tasks/<int:task_id>/complete/", CompleteTaskView.as_view(), name="complete-task"),
]


#   DO
urlpatterns+=[
    path('add_do/', AddDoAPIView.as_view()),
    path('get_do_list/', ListDoAPIView.as_view()),

]


# PROGRAM
urlpatterns+=[
    path('get_program_list/', ListProgramAPIView.as_view()),
]


# COMPLATE TASK
urlpatterns+=[
    path("tasks/completed/time/today-count/", UserTaskHistoryView.as_view()),
    path("tasks/completed/today-count/", TodayCompletedTasksCountView.as_view()),
    path('stats/weekly/', WeeklyCompleteTaskAPIView.as_view(), name='weekly-complete-tasks'),
    path('stats/monthly/', MonthlyCompleteTaskAPIView.as_view(), name='monthly-complete-tasks'),
    path('stats/yearly/', YearlyCompleteTaskAPIView.as_view(), name='yearly-complete-tasks'),
]

