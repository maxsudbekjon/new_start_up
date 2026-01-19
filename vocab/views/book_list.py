from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from vocab.models.book import Book
from vocab.serializers import BookModelSerializer


class BookListAPIView(generics.ListAPIView):
    queryset=Book.objects.all()
    serializer_class=BookModelSerializer
    permission_classes=[IsAuthenticated]