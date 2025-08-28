from rest_framework import generics
from vocab.models import Language
from vocab.serializers import LanguageSerializer

class LanguageListAPIView(generics.ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class LanguageCreateAPIView(generics.CreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer