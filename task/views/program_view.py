import random
import PyPDF2
from rest_framework.views import APIView
from rest_framework.response import Response
from task.models.complete_task import CompleteTask
from task.serializers.program import ProgramSerializer
from rest_framework.permissions import IsAuthenticated
from task.models.task import Program, Task
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from django.utils import timezone
from task.serializers.task_serializer import  VocabSerializer
from vocab.models.book import Book, BookProgress
from vocab.models.vocab import Vocab







@extend_schema(tags=["Task yaratish"])
class ListProgramAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "not any program found"}, status=200)
        return super().list(request, *args, **kwargs)


class GetTaskProgram(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, program=None):
        path_program = program or request.query_params.get("program")

        filters = {"user": request.user, "is_active": True}
        if path_program:
            filters["program__title"] = path_program

        task = Task.objects.filter(**filters).first()
        if not task:
            return Response({"error": "task topilmadi"}, status=404)

        # ✅ Tekshiramiz: user bugun bu taskni bajarganmi?
        today = timezone.now().date()
        already_completed = CompleteTask.objects.filter(
            user=request.user,
            task=task,
            completed_at__date=today
        ).exists()

        if already_completed:
            return Response({"message": "Siz bugun bu programdagi taskni allaqachon bajargansiz."}, status=200)

        # Userning o‘z tasklari (oddiy nomlarini chiqaramiz)
        user_tasks = list(Task.objects.filter(user=request.user).values_list("title__title", flat=True))
        result = {"user_tasks": user_tasks}

        # Task title orqali aniqlash
        task_title = task.title.title.lower()

        if getattr(task, "language", None) is not None:
            vocabs = Vocab.objects.filter(language=task.language)
            vocabs = random.sample(list(vocabs), min(len(vocabs), task.count))
            result["vocabs"] = VocabSerializer(vocabs, many=True).data
            return Response(result, status=200)

        elif getattr(task, "book", None) is not None:
            progress, _ = BookProgress.objects.get_or_create(user=request.user, book=task.book)
            pages_text = []

            with open(task.book.book.path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                total_pages = len(reader.pages)

                start_page = progress.last_page + 1
                end_page = progress.last_page + task.count

                if end_page > total_pages:
                    return Response({"error": f"Kitobning jami {total_pages} sahifasi bor"}, status=400)

                for k in range(start_page - 1, end_page):
                    text = reader.pages[k].extract_text()
                    pages_text.append({"page": k + 1, "content": text})

                progress.last_page = end_page
                progress.save()

            result.update({
                "book": task.book.name,
                "total_pages": total_pages,
                "start_page": start_page,
                "end_page": progress.last_page,
                "pages": pages_text
            })
            return Response(result, status=200)

        
        else:
            result["task"] = task_title
            return Response(result, status=200)


@extend_schema(tags=["Task yaratish"])
class GetVocabProgram(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, program=None):
        path_program = program or request.query_params.get("program")

        filters = {"user": request.user, "is_active": True}
        if path_program:
            filters["program__title"] = path_program

        task = Task.objects.filter(**filters).first()
        if not task:
            return Response({"error": "task topilmadi"}, status=404)

        requested_count = request.query_params.get("count")
        if requested_count is not None:
            try:
                requested_count = int(requested_count)
            except (TypeError, ValueError):
                return Response({"error": "count raqam bo'lishi kerak"}, status=400)
            if requested_count <= 0:
                return Response({"error": "count 0 dan katta bo'lishi kerak"}, status=400)

        count = requested_count if requested_count is not None else task.count

        vocabs = Vocab.objects.all()
        if getattr(task, "language", None) is not None:
            vocabs = vocabs.filter(language=task.language)

        vocabs = list(vocabs)
        if not vocabs:
            return Response({"error": "vocab topilmadi"}, status=404)

        sample_count = min(len(vocabs), count)
        vocabs = random.sample(vocabs, sample_count)

        return Response({
            "task": task.title.title,
            "program": task.program.title,
            "count": sample_count,
            "vocabs": VocabSerializer(vocabs, many=True).data
        }, status=200)
