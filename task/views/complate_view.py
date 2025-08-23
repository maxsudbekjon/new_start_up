from rest_framework import generics
from task.models import CompleteTask
from task.serializers.complete_task_serializer import CompleteTaskSerializer


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = CompleteTask.objects.all()
    serializer_class = CompleteTaskSerializer
