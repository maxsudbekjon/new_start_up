from rest_framework import serializers
from task.models.do import Do

class DoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Do
        fields = ('title', 'description')