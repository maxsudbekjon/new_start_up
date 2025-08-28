from rest_framework import serializers
from vocab.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'name',
            'description',
            'link'
        )