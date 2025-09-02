from rest_framework import serializers
from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'user',
            'title',
            'program',
            'count',
            'duration',
            'is_active'
        )
        read_only_fields = ['user']
