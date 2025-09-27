from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from task.serializers.program import ProgramSerializer
from task.models.task import Program, Task
from vocab.models.language import Language
from vocab.models.vocab import Vocab
from vocab.serializers.vocab_serializer import VocabSerializer
import random


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


class GetTaskProgram(APIView):
    # permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Task bo‘yicha random vocablarni olish",
        description="Program va language bo‘yicha filterlab, tasodifiy vocablarni qaytaradi.",
        parameters=[
            OpenApiParameter(
                name="program",
                description="Program nomi",
                required=False,
                type=str,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name="language",
                description="Til nomi (english, russian, arabic, turkish)",
                required=False,
                type=str,
                location=OpenApiParameter.QUERY
            ),
        ],
        responses={
            200: OpenApiResponse(response=VocabSerializer(many=True), description="Tasodifiy vocablar"),
            400: OpenApiResponse(description="Xato so‘rov"),
        },
    )
    def get(self, request):
        path_program = request.query_params.get("program")
        path_language = request.query_params.get("language")

        filters = {
            "user": request.user,
            "is_complete": False,
        }

        if path_program:
            filters["program__title"] = path_program
        if path_language:
            filters["title__language__name"] = path_language

        tasks = Task.objects.filter(**filters)

        if not tasks.exists():
            return Response({"error": "task topilmadi"})

        task = tasks.first()

        if task.title.language.name == path_language:
            vocabs = Vocab.objects.filter(language__name=path_language)
            vocabs = random.sample(list(vocabs), min(len(vocabs), task.count))
            serializer = VocabSerializer(vocabs, many=True).data
            return Response(serializer, status=200)
        else:
            return Response({"error": "bunday til yoq"})
