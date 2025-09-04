from django.urls import path
from task.views.complate_view import AddCompleteTaskAPIView, GetAllCompleteTaskAPIView
from task.views.do_view import AddDoAPIView, ListDoAPIView
from task.views.program_view import AddProgramAPIView, ListProgramAPIView
from task.views.task_view import AddTaskAPIView, ListTaskAPIView, UpdateTaskAPIView, DeleteTaskAPIView


urlpatterns = [
    path('add_complete_task/', view=AddCompleteTaskAPIView.as_view()),
    path('list_complete_task/', GetAllCompleteTaskAPIView.as_view()),

    path('add_do/', AddDoAPIView.as_view()),
    path('get_do_list/', ListDoAPIView.as_view()),

    path('add_program/', AddProgramAPIView.as_view()),
    path('get_program_list/', ListProgramAPIView.as_view()),

    path('add_task/', AddTaskAPIView.as_view()),
    path('get_task_list/', ListTaskAPIView.as_view()),
    path('update_task/<int:pk>/', UpdateTaskAPIView.as_view()),
    path('delete_task/<int:pk>/', DeleteTaskAPIView.as_view()),


]
