from rest_framework import serializers
from task.models import Task, Program, Do

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'title',
            'program',
            'count',
            'duration',
            'is_active'
        )

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('title', 'image')

class DoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Do
        fields = ('title', 'description')