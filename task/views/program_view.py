from rest_framework.views import APIView
from rest_framework.response import Response
from task.serializers.program import ProgramSerializer
from rest_framework.permissions import IsAuthenticated
from task.models.task import Program
from drf_spectacular.utils import extend_schema
from rest_framework import generics

@extend_schema(tags=["program"])
class ListProgramAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "not any program found"}, status=200)
        return super().list(request, *args, **kwargs)




