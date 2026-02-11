from dateutil.utils import today
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from task.serializers import CompleteTaskSerializer
from task.serializers.complete_task_serializer import TaskCompleteForSerializer
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
            return Response({"error": "task not found"}, status=404),


@extend_schema(tags=["Task bajarish uchun ketgan vaqt"], request=ComplatetasTimeSerializer)
class CompleteTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        serializer = ComplatetasTimeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = Task.objects.filter(id=task_id, user=request.user).first()
        if not task:
            return Response({"error": "Task topilmadi"}, status=404)

        start_time = serializer.validated_data["start_time"]
        end_time = serializer.validated_data["end_time"]

        spent_time = int((end_time - start_time).total_seconds())

        today = timezone.localdate()

        with transaction.atomic():
            qs = (
                CompleteTask.objects
                .select_for_update()
                .filter(user=request.user, task=task, completed_at__date=today)
                .order_by("id")
            )

            complete_task = qs.first()
            if complete_task is None:
                complete_task = CompleteTask.objects.create(
                    user=request.user,
                    task=task,
                    spent_time=spent_time,
                )
            else:
                # Clean duplicates if they exist for the same day.
                qs.exclude(id=complete_task.id).delete()
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
            "task_id": task.id,
            "spent_time_seconds": spent_time,
            "completed_date": today
        }, status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@extend_schema(tags=["Tasklar ro'yxati"])
def complete_task(request):
    today = timezone.now().date()

    complete_tasks = CompleteTask.objects.filter(
        completed_at__date=today
    )

    serializer = TaskCompleteForSerializer(complete_tasks, many=True)
    return Response(serializer.data)
