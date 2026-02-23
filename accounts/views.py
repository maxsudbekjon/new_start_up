from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from accounts.models.profile import Profile
from drf_spectacular.utils import extend_schema
from accounts.models.rating import Rating
from accounts.serializers import CustomUserSerializer, ProfileSerializer, RatingSerializer, UserDetailModelSerializer, LoginSerializer, LogoutSerializer
from task.models.complete_task import CompleteTask
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import Sum, F, Q, Prefetch, Window
from django.db.models.functions import DenseRank
from datetime import timedelta
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()


@extend_schema(request=CustomUserSerializer)
class RegisterApiView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    # def post(self, request):
    #     serializer = CustomUserSerializer(data=request.data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=LogoutSerializer)
class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data["refresh"]
        token = RefreshToken(refresh)
        token.blacklist()

        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

@extend_schema(request=ProfileSerializer)
class UpdateUserProfileAPIView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Profile.objects.select_related("user"),
            user=self.request.user
        )

@extend_schema(tags=["User"])
class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserDetailModelSerializer

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserDetailModelSerializer(user)
        return Response(serializer.data)
    



class RatingPagination(PageNumberPagination):
    page_size = 10  # Har sahifada 10 ta foydalanuvchi
    page_size_query_param = 'page_size'
    max_page_size = 100

@extend_schema(tags=['reting'])
class GlobalRatingListView(ListAPIView):
    serializer_class = RatingSerializer
    pagination_class = RatingPagination

    def get_queryset(self):
        return (
            Profile.objects
            .select_related('user')
            .annotate(rank=Window(expression=DenseRank(), order_by=F('score').desc()))
            .order_by('-score', 'id')
        )
    

@extend_schema(tags=['reting'])
class MonthlyRatingListView(ListAPIView):
    serializer_class = RatingSerializer
    pagination_class = RatingPagination

    def get_queryset(self):
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return (
            Profile.objects
            .select_related('user')
            .filter(rating__created_at__gte=month_start)
            .annotate(score=Sum('rating__point', filter=Q(rating__created_at__gte=month_start)))
            .annotate(rank=Window(expression=DenseRank(), order_by=F('score').desc()))
            .order_by('-score', 'id')
        )



@extend_schema(tags=['reting'])
class StreakRatingListView(ListAPIView):
    serializer_class = RatingSerializer
    pagination_class = RatingPagination

    def get_queryset(self):
        lookback_days = 90
        cutoff = timezone.now() - timedelta(days=lookback_days)
        completions_qs = (
            CompleteTask.objects
            .filter(completed_at__gte=cutoff)
            .only("completed_at", "user_id")
            .order_by("-completed_at")
        )
        profiles = list(
            Profile.objects
            .select_related('user')
            .prefetch_related(
                Prefetch(
                    "user__completetask_set",
                    queryset=completions_qs,
                    to_attr="recent_completions",
                )
            )
        )

        data = []
        for profile in profiles:
            completions = getattr(profile.user, "recent_completions", [])
            streak = self.calculate_streak(completions)
            profile.score = streak
            data.append(profile)

        data.sort(key=lambda p: p.score, reverse=True)
        current_rank = 0
        last_score = None
        for idx, profile in enumerate(data, start=1):
            if profile.score != last_score:
                current_rank = idx
                last_score = profile.score
            profile.rank = current_rank

        return data

    def calculate_streak(self, completions):
        if not completions:
            return 0

        streak = 1
        prev_date = completions[0].completed_at.date()

        for comp in completions[1:]:
            current_date = comp.completed_at.date()
            diff = (prev_date - current_date).days
            if diff == 1:
                streak += 1
                prev_date = current_date
            elif diff == 0:
                continue
            else:
                break
        return streak
