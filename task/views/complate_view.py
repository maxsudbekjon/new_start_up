from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from task.models import CompleteTask
from drf_spectacular.utils import extend_schema
from datetime import  timedelta
from django.utils.timezone import now
import calendar







@extend_schema(tags=["Bosh sahifa"])
class TodayCompletedTasksCountView(APIView):
    permission_classes = [IsAuthenticated]  # faqat login bo‘lgan user ko‘ra oladi

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
        today = timezone.now().date()  # bugungi sana

        completed = CompleteTask.objects.filter(
            user=request.user,
            completed_at__date=today   # faqat bugungi
        ).values(
            "spent_time", 
        )

        return Response(list(completed), status=200)


@extend_schema(tags=["Statistika"])
class WeeklyCompleteTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday() + 7)
        end_of_week = start_of_week + timedelta(days=6)

        queryset = CompleteTask.objects.filter(user=user, completed_at__date__range=[start_of_week, end_of_week])
        
        if not queryset.exists():
            return None

        daily_stats = []
        for i in range(7):
            day_date = start_of_week + timedelta(days=i)
            count = queryset.filter(completed_at__date=day_date).count()
            daily_stats.append({
                "day": calendar.day_name[day_date.weekday()],
                "date": str(day_date),
                "count": count
            })
        return Response(daily_stats)
    

@extend_schema(tags=["Statistika"])
class MonthlyCompleteTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = now().date()
        first_day_this_month = today.replace(day=1)
        last_month_last_day = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_month_last_day.replace(day=1)

        queryset = CompleteTask.objects.filter(
            user=user,
            completed_at__date__range=[first_day_last_month, last_month_last_day]
        )

        if not queryset.exists():
            return None

        monthly_stats = []
        for week_num in range(1, 5):
            week_start = first_day_last_month + timedelta(days=(week_num-1)*7)
            week_end = week_start + timedelta(days=6)
            if week_end > last_month_last_day:
                week_end = last_month_last_day
            count = queryset.filter(completed_at__date__range=[week_start, week_end]).count()
            monthly_stats.append({
                "week": week_num,
                "month": first_day_last_month.strftime("%B"),
                "count": count
            })
        return Response(monthly_stats)
    

@extend_schema(tags=["Statistika"])
class YearlyCompleteTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = now().date()
        last_year = today.year - 1

        queryset = CompleteTask.objects.filter(
            user=user,
            completed_at__year=last_year
        )

        if not queryset.exists():
            return None

        yearly_stats = []
        for month_num in range(1, 13):
            count = queryset.filter(completed_at__month=month_num).count()
            month_name = calendar.month_name[month_num]
            yearly_stats.append({
                "month": month_name,
                "year": last_year,
                "count": count
            })
        return Response(yearly_stats)









# @extend_schema(tags=["Complate Tasks"])
# class GetAllCompleteTaskAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CompleteTaskSerializer
#     queryset = CompleteTask.objects.all()

#     def get_queryset(self):
#         return self.queryset.filter(task__user=self.request.user)