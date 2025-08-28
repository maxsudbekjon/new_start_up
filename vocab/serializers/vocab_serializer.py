from rest_framework import serializers
from vocab.models import Vocab

class VocabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocab
        fields = (
            "image",
            'word_1',
            'word_uz',
            'text'
        )