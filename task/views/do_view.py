from rest_framework.views import APIView
from rest_framework.response import Response
from task.serializers.do_serializer import DoSerializer
from rest_framework.permissions import IsAuthenticated
from task.models.task import Do
from drf_spectacular.utils import extend_schema
from rest_framework import generics




@extend_schema(tags=["Task yaratish"], request=DoSerializer)
class AddDoAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DoSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@extend_schema(tags=["Task yaratish"])
class ListDoAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DoSerializer

    def get(self, request):
        do_list = Do.objects.all()
        if not do_list:
            return Response({"error": "not any Do found.!"}, status=404)
        serializer = self.get_serializer(do_list, many=True)
        return Response(serializer.data, status=200)
