from dateutil.utils import today
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from task.serializers import CompleteTaskSerializer
from task.serializers.task_serializer import ComplatetasTimeSerializer, ListTaskSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated
from task.models.task import Task
from task.models.complete_task import CompleteTask
from accounts.models.profile import Profile
from accounts.models.rating import Rating
from django.db import transaction
from django.db.models import F
import datetime
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from task.services.task_limits import validate_task_count







@extend_schema(tags=["Task yaratish"], request=TaskSerializer)
class AddTaskAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        result = validate_task_count(
            user=request.user,
            program=serializer.validated_data["program"],
            count=serializer.validated_data["count"],
        )

        if not result.allowed:
            return Response(
                {"message": result.message},
                status=status.HTTP_400_BAD_REQUEST
            )

        task = serializer.save(user=request.user)

        response_serializer = self.get_serializer(task)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


@extend_schema(tags=["Tasklar ro'yxati"])
class ListTaskAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListTaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


@extend_schema(tags=["Tasklar ro'yxati"], request=TaskSerializer)
class UpdateTaskAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


@extend_schema(tags=["Tasklar ro'yxati"])
class DeleteTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
            task.delete()
            return Response({"message": "task deleted successfully"}, status=200)
        except Task.DoesNotExist:
            return Response({"error": "task not found"}, status=404)


@extend_schema(tags=["Task bajarish uchun ketgan vaqt"], request=ComplatetasTimeSerializer)
class CompleteTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        serializer = ComplatetasTimeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        task = Task.objects.filter(id=task_id, user=request.user).first()
        if not task:
            return Response({"error": "Task topilmadi"}, status=404)

        # Boshlanish va tugash vaqtlarini olish
        # task.is_complete = True
        # task.save(update_fields=["is_complete"])
        start_time = serializer.validated_data.get("start_time")  # int (timestamp)
        end_time = serializer.validated_data.get("end_time")      # int (timestamp)

        if not start_time or not end_time:
            return Response({"error": "start_time va end_time yuboring"}, status=400)

        start_minutes = start_time.hour * 60 + start_time.minute
        end_minutes = end_time.hour * 60 + end_time.minute

        spent_time = end_minutes - start_minutes  # sekundlarda hisoblash

        with transaction.atomic():
            complete_task, created = CompleteTask.objects.get_or_create(
                user=request.user,
                task=task,
                defaults={"spent_time": spent_time},
            )
            if not created and complete_task.spent_time != spent_time:
                complete_task.spent_time = spent_time
                complete_task.save(update_fields=["spent_time"])

            profile, _ = Profile.objects.get_or_create(
                user=request.user,
                defaults={"bio": "this is my bio"},
            )
            Profile.objects.filter(id=profile.id).update(score=F("score") + 5)
            Rating.objects.create(point=5, user_profile=profile)

        return Response({
            "message": "Task tugallandi",
            "task": task.title.title,
            "spent_time": spent_time
        }, status=201)


@api_view(["GET"])
@extend_schema(tags=["Tasklar ro'yxati"])
def complete_task(request):
    today = timezone.now().date()

    complete_tasks = CompleteTask.objects.filter(
        completed_at__date=today
    )

    serializer = TaskCompleteForSerializer(complete_tasks, many=True)
    return Response(serializer.data)
