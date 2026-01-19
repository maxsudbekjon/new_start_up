from rest_framework.views import APIView
from rest_framework.response import Response
from task.serializers.do_serializer import DoSerializer
from rest_framework.permissions import IsAuthenticated
from task.models.task import Do
from drf_spectacular.utils import extend_schema
from rest_framework import generics




@extend_schema(tags=["Task"])
class AddDoAPIView(generics.CreateAPIView):
    queryset = Do.objects.all()
    serializer_class = DoSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["Task"])
class ListDoAPIView(generics.ListAPIView):
    queryset=Do.objects.all()
    serializer_class=DoSerializer
    permission_classes=[IsAuthenticated]