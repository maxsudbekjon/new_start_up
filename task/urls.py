from django.urls import path
from task.views.complate_view import WeeklyStatisticAPIView, \
    MonthlyStatisticAPIView, YearlyStatisticAPIView
from task.views.do_view import AddDoAPIView, ListDoAPIView
from task.views.program_view import AddProgramAPIView, ListProgramAPIView, GetTaskProgram
from task.views.task_view import AddTaskAPIView, ListTaskAPIView, UpdateTaskAPIView, DeleteTaskAPIView
from vocab.views.book_view import BookPageAPIView


urlpatterns = [
    path('get_weekly_statistics/', WeeklyStatisticAPIView.as_view()),
    path('get_monthly_statistics/', MonthlyStatisticAPIView.as_view()),
    path('get_yearly_statistics/', YearlyStatisticAPIView.as_view()),


    path('add_do/', AddDoAPIView.as_view()),
    path('get_do_list/', ListDoAPIView.as_view()),

    path('add_program/', AddProgramAPIView.as_view()),
    path('get_program_list/', ListProgramAPIView.as_view()),
    path('get_task_program/', GetTaskProgram.as_view()),


    path('add_task/', AddTaskAPIView.as_view()),
    path('get_task_list/', ListTaskAPIView.as_view()),
    path('update_task/<int:pk>/', UpdateTaskAPIView.as_view()),
    path('delete_task/<int:pk>/', DeleteTaskAPIView.as_view()),

    path('get_book/<int:pk>/', BookPageAPIView.as_view(), ),


]
