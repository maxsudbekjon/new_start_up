from rest_framework import serializers
from task.models.task import Do





class DoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Do
        fields = ("id", "title", "description")
        read_only_fields = ("id",)

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title juda qisqa")
        return value

