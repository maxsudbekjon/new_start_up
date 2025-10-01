from rest_framework.views import APIView
from rest_framework.response import Response
from task.serializers.task_serializer import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from task.models.task import Task
from task.models.complete_task import CompleteTask
from task.utils import calculate_streak
from drf_spectacular.utils import extend_schema
from rest_framework import generics
@extend_schema(tags=["Task"], request=TaskSerializer)
class AddTaskAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            user_age = request.user.age
            count = serializer.validated_data.get('count')
            a = 5
            b = 10
            c = 15
            completions = (
                CompleteTask.objects.filter(user=request.user).order_by("completed_at").values_list("completed_at", flat=True)
            )
            max_value = calculate_streak(list(completions))

            if max_value >= 1:
                a += 3
                b += 3
                c += 3

            if user_age <= 10 and count > a:
                return Response({"message": f"10 yoshdan kichiklar uchun maksimal {a}"}, status=400)
            elif 10 < user_age < 20 and count > b:
                return Response({"message": f"10 va 19 yoshgacha maksimal {b}"}, status=400)
            elif user_age >= 20 and count > c:
                return Response({"message": f"20 yoshdan kattalar uchun maksimal {c}"}, status=400)

            task = serializer.save(user=request.user)
            return Response(self.get_serializer(task).data, status=201)
        return Response(serializer.errors, status=400)

@extend_schema(tags=["Task"])
class ListTaskAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

@extend_schema(tags=["Task"], request=TaskSerializer)
class UpdateTaskAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


@extend_schema(tags=["Task"])
class DeleteTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
            task.delete()
            return Response({"message": "task deleted successfully"}, status=200)
        except Task.DoesNotExist:
            return Response({"error": "task not found"}, status=404)


class CompleteTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        task = Task.objects.filter(id=task_id, user=request.user).first()
        if not task:
            return Response({"error": "Task topilmadi"}, status=404)

        # Boshlanish va tugash vaqtlarini olish
        start_time = request.data.get("start_time")  # frontend yuboradi (timestamp)
        end_time = request.data.get("end_time")      # frontend yuboradi (timestamp)

        if not start_time or not end_time:
            return Response({"error": "start_time va end_time yuboring"}, status=400)

        spent_time = int(end_time) - int(start_time)  # sekundda hisoblaymiz

        complete_task = CompleteTask.objects.create(
            user=request.user,
            task=task,
            spent_time=spent_time
        )

        return Response({
            "message": "Task tugallandi",
            "task": task.title.title,
            "spent_time": spent_time
        }, status=201)
