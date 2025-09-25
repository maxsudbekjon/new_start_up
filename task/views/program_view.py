from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from drf_spectacular.types import OpenApiTypes
from task.serializers.program import ProgramSerializer
from task.models.task import Program


class AddProgramAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Upload an image ",
        description="Upload image file",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "image": {"type": "string", "format": "binary"},
                },
                "required": ["title", "image"],
            }
        },
        responses={200: OpenApiTypes.OBJECT},
    )
    def post(self, request):
        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ListProgramAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=ProgramSerializer(many=True),
        summary="Programlar ro‘yxati"
    )
    def get(self, request):
        programs = Program.objects.all()
        if not programs:
            return Response({"message": "not any program found"})
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data, status=200)
