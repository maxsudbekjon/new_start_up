from rest_framework.views import APIView
from rest_framework.response import Response
from task.serializers.task_serializer import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from task.models.task import Task


class AddTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ListTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)

        # if not tasks.exists():
        #     return Response({"message": "you have not any task.!"}, status=404)

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
