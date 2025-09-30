from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from task.models import CompleteTask
import datetime


class WeeklyStatisticAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Haftalik statistika",
        description="Foydalanuvchining joriy hafta davomida tugatgan vazifalari sonini qaytaradi.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "week": {"type": "integer", "example": 39},
                    "count": {"type": "integer", "example": 12}
                }
            }
        }
    )
    def get(self, request):
        today = datetime.datetime.today()
        current_week = today.isocalendar()[1]

        queryset = CompleteTask.objects.filter(
            user=request.user,
            completed_at__week=current_week,
            completed_at__year=today.year
        )

        count = queryset.count()

        return Response(
            {
                "week": current_week,
                "count": count
            }
        )


class MonthlyStatisticAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Oylik statistika",
        description="Foydalanuvchining joriy oy davomida tugatgan vazifalari sonini qaytaradi.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "month": {"type": "integer", "example": 9},
                    "count": {"type": "integer", "example": 45}
                }
            }
        }
    )
    def get(self, request):
        today = datetime.datetime.today()
        current_month = today.month

        queryset = CompleteTask.objects.filter(
            user=request.user,
            completed_at__month=current_month,
            completed_at__year=today.year
        )

        count = queryset.count()

        return Response(
            {
                "month": current_month,
                "count": count
            }
        )


class YearlyStatisticAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Yillik statistika",
        description="Foydalanuvchining joriy yil davomida tugatgan vazifalari sonini qaytaradi.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "year": {"type": "integer", "example": 2025},
                    "count": {"type": "integer", "example": 320}
                }
            }
        }
    )
    def get(self, request):
        today = datetime.datetime.today()
        current_year = today.year

        queryset = CompleteTask.objects.filter(
            user=request.user,
            completed_at__year=current_year
        )

        count = queryset.count()

        return Response(
            {
                "year": current_year,
                "count": count
            }
        )
