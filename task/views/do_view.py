from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from task.serializers.do_serializer import DoSerializer
from task.models.task import Do


class AddDoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=DoSerializer,
        responses=DoSerializer,
        summary="Yangi Do qo‘shish"
    )
    def post(self, request):
        serializer = DoSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class ListDoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=DoSerializer(many=True),
        summary="Do ro‘yxati"
    )
    def get(self, request):

        do_list = Do.objects.filter(
            Q(user__isnull=True) | Q(user=request.user)  # admin Do lar + user Do lar
        )

        if not do_list.exists():
            return Response({"error": "not any Do found.!"})
        serializer = DoSerializer(do_list, many=True)
        return Response(serializer.data, status=200)
