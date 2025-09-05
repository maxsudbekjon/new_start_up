from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from task.models import CompleteTask
from task.serializers.complete_task_serializer import CompleteTaskSerializer


# class AddCompleteTaskAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         serializer = CompleteTaskSerializer(data=request.data)
#
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


class GetAllCompleteTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        complete_tasks = CompleteTask.objects.filter(task__user=request.user)

        serializer = CompleteTaskSerializer(complete_tasks, many=True)
        return Response(serializer.data, status=200)
