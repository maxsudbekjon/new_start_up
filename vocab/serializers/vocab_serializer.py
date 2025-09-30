from rest_framework import serializers
from vocab.models.vocab import Vocab


class VocabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocab
        fields = ['id', "image", 'word_1', "word_uz", "text_1", "text_uz", "audio", "language"]



