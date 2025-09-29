from rest_framework import serializers
from task.models.task import Do


class DoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Do
        fields = ('id', 'user', 'title', 'description')

        read_only_fields = ['user']
