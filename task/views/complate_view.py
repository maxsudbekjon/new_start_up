from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from task.models import CompleteTask
from task.serializers.complete_task_serializer import CompleteTaskSerializer
from django.utils.dateparse import parse_date
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(tags=["Complate Tasks"])
class GetAllCompleteTaskAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompleteTaskSerializer
    queryset = CompleteTask.objects.all()

    def get_queryset(self):
        return self.queryset.filter(task__user=self.request.user)

@extend_schema(tags=["Complate Tasks"])
class CompleteTaskStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name="date", description="YYYY-MM-DD formatida kunlik statistika", required=False, type=str),
            OpenApiParameter(name="month", description="YYYY-MM formatida oylik statistika", required=False, type=str),
            OpenApiParameter(name="year", description="YYYY formatida yillik statistika", required=False, type=str),
        ],
        summary="CompleteTask statistikasi",
        description="Kunlik, oylik yoki yillik statistikani qaytaradi."
    )
    def get(self, request):
        user = request.user
        date = request.query_params.get("date")
        month = request.query_params.get("month")
        year = request.query_params.get("year")

        queryset = CompleteTask.objects.filter(user=user)

        if date:
            queryset = queryset.filter(completed_at__date=parse_date(date))
            serializer = CompleteTaskSerializer(queryset, many=True)
            return Response({
                "type": "daily",
                "date": date,
                "tasks": serializer.data,
                "count": queryset.count()
            })

        elif month:
            year, month_num = month.split("-")
            queryset = queryset.filter(
                completed_at__year=int(year),
                completed_at__month=int(month_num)
            )
            serializer = CompleteTaskSerializer(queryset, many=True)
            return Response({
                "type": "monthly",
                "month": month,
                "tasks": serializer.data,
                "count": queryset.count()
            })

        elif year:
            queryset = queryset.filter(completed_at__year=int(year))
            serializer = CompleteTaskSerializer(queryset, many=True)
            return Response({
                "type": "yearly",
                "year": year,
                "tasks": serializer.data,
                "count": queryset.count()
            })

        return Response({"error": "date, month yoki year query param bering"}, status=400)
