from rest_framework import generics
from vocab.models import Vocab
from vocab.serializers import VocabSerializer

class VocabListAPIView(generics.ListAPIView):
    queryset = Vocab.objects.all()
    serializer_class = VocabSerializer

class VocabCreateAPIView(generics.CreateAPIView):
    queryset = Vocab.objects.all()
    serializer_class = VocabSerializer

