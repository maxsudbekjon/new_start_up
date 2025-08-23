from rest_framework import serializers
from task.models.program import Program

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('title', 'image')