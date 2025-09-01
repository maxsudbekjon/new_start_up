from rest_framework import serializers
from task.models.base import BasicClass


class BasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicClass
        fields = ('created_at', 'updated_at')