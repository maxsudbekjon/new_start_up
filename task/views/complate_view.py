from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from task.models import CompleteTask
from task.serializers.complete_task_serializer import CompleteTaskSerializer
from django.utils.dateparse import parse_date


class GetAllCompleteTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        complete_tasks = CompleteTask.objects.filter(task__user=request.user)

        serializer = CompleteTaskSerializer(complete_tasks, many=True)
        return Response(serializer.data, status=200)


class CompleteTaskStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        date = request.query_params.get("date")
        month = request.query_params.get("month")
        year = request.query_params.get("year")

        queryset = CompleteTask.objects.filter(user=user)

        # Kunlik statistika
        if date:
            queryset = queryset.filter(completed_at__date=parse_date(date))
            serializer = CompleteTaskSerializer(queryset, many=True)
            return Response({
                "type": "daily",
                "date": date,
                "tasks": serializer.data,  # yoki serializer ishlatish mumkin
                "count": queryset.count()
            })

        # Oylik statistika
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

        # Yillik statistika
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
