from rest_framework import serializers

from vocab.models.book import Book


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields="__all__"
