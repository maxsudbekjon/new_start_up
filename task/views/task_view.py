from rest_framework.views import APIView
from rest_framework.response import Response
from task.serializers.task_serializer import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from task.models.task import Task
from task.models.complete_task import CompleteTask
from task.utils import calculate_streak


class AddTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={"request": request})

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
                return Response({"message": f"10 yoshdan kichiklar uchun maksimal {a}"})
            elif 10 < user_age < 20 and count > b:
                return Response({"message": f"10 va 19 yoshgacha maksimal {b}"})
            elif user_age >= 20 and count > c:
                return Response({"message": f"20 yoshdan kattalar uchun maksimal {c}"})

            task = serializer.save(user=request.user)
            return Response(TaskSerializer(task).data, status=201)

        return Response(serializer.errors, status=400)


class ListTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class UpdateTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)

        except Task.DoesNotExist:
            return Response({"message": "not found"}, status=404)

        serializer = TaskSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class DeleteTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:
            task = Task.objects.get(pk=pk, user=request.user)
            task.delete()
            return Response({"message": "task deleted successfully"}, status=200)
        except Task.DoesNotExist:
            return Response({"error": "task not found"}, status=404)


