from rest_framework import generics
from task.models import Task, Program, Do
from task.serializers.task_serializer import TaskSerializer ,ProgramSerializer, DoSerializer

class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class ProgramCreatAPIView(generics.CreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

class DoCreatAPIView(generics.CreateAPIView):
    queryset = Do.objects.all()
    serializer_class = DoSerializer