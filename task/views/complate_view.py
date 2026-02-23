from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from task.models import CompleteTask
from drf_spectacular.utils import extend_schema
from datetime import  timedelta
import calendar
from rest_framework import status
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncMonth




@extend_schema(tags=["Bosh sahifa"])
class TodayCompletedTasksCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        count = CompleteTask.objects.filter(
            user=request.user,
            completed_at__date=today
        ).count()
        return Response({"today_completed_tasks_count": count})
    

@extend_schema(tags=["Bosh sahifa"])
class UserTaskHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()

        completed = CompleteTask.objects.filter(
            user=request.user,
            completed_at__date=today
        ).values(
            "spent_time", 
        )

        return Response(list(completed), status=200)


@extend_schema(tags=["Statistika"])
class WeeklyCompleteTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        today = timezone.localdate()
        start_of_week = today - timedelta(days=today.weekday() + 7)  # o'tgan hafta dushanba
        end_of_week = start_of_week + timedelta(days=6)             # o'tgan hafta yakshanba

        # ✅ 1 ta query: kunlar bo'yicha guruhlab sanab beradi
        qs = (
            CompleteTask.objects
            .filter(user=user, completed_at__date__range=[start_of_week, end_of_week])
            .annotate(day=TruncDate("completed_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        # qs -> [{'day': date, 'count': n}, ...]
        counts_by_day = {row["day"]: row["count"] for row in qs}

        # ✅ bo'sh kunlarni ham 0 bilan to'ldiramiz
        daily_stats = []
        for i in range(7):
            day_date = start_of_week + timedelta(days=i)
            daily_stats.append({
                "day": calendar.day_name[day_date.weekday()],
                "date": str(day_date),
                "count": counts_by_day.get(day_date, 0)
            })

        if sum(item["count"] for item in daily_stats) == 0:
            return Response({"message": "O‘tgan hafta bajarilgan topshiriqlar yo‘q."}, status=status.HTTP_200_OK)

        return Response(daily_stats, status=status.HTTP_200_OK)


@extend_schema(tags=["Statistika"])
class MonthlyCompleteTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        today = timezone.localdate()
        first_day_this_month = today.replace(day=1)
        last_month_last_day = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_month_last_day.replace(day=1)

        # ✅ 1 ta query: o'tgan oy ichidagi kunlar bo'yicha guruhlab sanash
        qs = (
            CompleteTask.objects
            .filter(user=user, completed_at__date__range=[first_day_last_month, last_month_last_day])
            .annotate(day=TruncDate("completed_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        # Kunlar kesimida dict
        counts_by_day = {row["day"]: row["count"] for row in qs}

        # ✅ "oy ichidagi hafta" (1-hafta, 2-hafta, ...) ni Python'da hisoblaymiz
        total_days = (last_month_last_day - first_day_last_month).days + 1
        weeks_count = (total_days + 6) // 7  # ceil

        weekly_buckets = [0] * weeks_count  # index 0 -> 1-hafta

        for day, cnt in counts_by_day.items():
            week_num = ((day - first_day_last_month).days // 7) + 1
            weekly_buckets[week_num - 1] += cnt

        if sum(weekly_buckets) == 0:
            return Response({"message": "O‘tgan oyda bajarilgan topshiriqlar yo‘q."}, status=status.HTTP_200_OK)

        month_name = first_day_last_month.strftime("%B")
        monthly_stats = [
            {"week": i + 1, "month": month_name, "count": weekly_buckets[i]}
            for i in range(weeks_count)
        ]

        return Response(monthly_stats, status=status.HTTP_200_OK)


@extend_schema(tags=["Statistika"])
class YearlyCompleteTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        today = timezone.localdate()
        last_year = today.year - 1

        # ✅ 1 ta query: oylar bo'yicha guruhlab sanash
        qs = (
            CompleteTask.objects
            .filter(user=user, completed_at__year=last_year)
            .annotate(month=TruncMonth("completed_at"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        # {'2025-01-01': 10, '2025-02-01': 3, ...} ko'rinishiga keltiramiz
        counts_by_month = {row["month"].month: row["count"] for row in qs}

        yearly_stats = []
        for month_num in range(1, 13):
            yearly_stats.append({
                "month": calendar.month_name[month_num],
                "year": last_year,
                "count": counts_by_month.get(month_num, 0)
            })

        if sum(item["count"] for item in yearly_stats) == 0:
            return Response({"message": "O‘tgan yil bajarilgan topshiriqlar yo‘q."}, status=status.HTTP_200_OK)

        return Response(yearly_stats, status=status.HTTP_200_OK)






# @extend_schema(tags=["Complate Tasks"])
# class GetAllCompleteTaskAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CompleteTaskSerializer
#     queryset = CompleteTask.objects.all()

#     def get_queryset(self):
#         return self.queryset.filter(task__user=self.request.user)