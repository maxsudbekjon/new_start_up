from rest_framework.views import APIView
from rest_framework.response import Response
from task.serializers.program import ProgramSerializer
from rest_framework.permissions import IsAuthenticated
from task.models.task import Program


class AddProgramAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProgramSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ListProgramAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        programs = Program.objects.all()

        if not programs:
            return Response({"message": "not any program found"})
        serializer = ProgramSerializer(programs, many=True)

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=200)




