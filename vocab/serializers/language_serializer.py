from rest_framework import serializers
from vocab.models import Language

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (
            'name',
            'vocab'
        )