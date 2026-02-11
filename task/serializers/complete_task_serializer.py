from rest_framework import serializers
from task.models.complete_task import CompleteTask





class CompleteTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompleteTask
        fields = (
            'id',
            'user',
            'task',
            'completed_at'
        )

class TaskCompleteForSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompleteTask
        fields = ('id',)