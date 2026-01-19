from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from vocab.models.book import Book
from vocab.serializers import BookModelSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Book"])
class BookListAPIView(generics.ListAPIView):
    queryset=Book.objects.all()
    serializer_class=BookModelSerializer
    permission_classes=[IsAuthenticated]
    