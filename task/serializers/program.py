from rest_framework import serializers
from task.models.task import Program


class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = ('id', 'title', 'image')
