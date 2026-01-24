from rest_framework import serializers

from vocab.models import Vocab
from vocab.models.book import Book


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields="__all__"

class VocabSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vocab
        fields="__all__"