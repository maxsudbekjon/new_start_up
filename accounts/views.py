from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from accounts.models.profile import Profile
from drf_spectacular.utils import extend_schema
from accounts.models.rating import Rating
from accounts.serializers import CustomUserSerializer, ProfileSerializer, RatingSerializer, UserDetailModelSerializer,LoginSerializer
from task.models.complete_task import CompleteTask
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
User = get_user_model()


@method_decorator(csrf_exempt, name='dispatch')
@extend_schema(request=CustomUserSerializer)
class RegisterApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema


@extend_schema(request=LoginSerializer)
class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            phone=phone,
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                "Login yoki parol noto‘g‘ri"
            )

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "phone": user.phone,
                "username": user.username,
            },
}     
@extend_schema(request=ProfileSerializer)
class UpdateUserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user_profile = Profile.objects.get(user=request.user)

        serializer = ProfileSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

@extend_schema(tags=["User"])
class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

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
        # Eng ko‘p ball to‘plaganlardan boshlab tartiblash
        return Profile.objects.select_related('user').order_by('-score')

    def get_serializer_context(self):
        # Reytingni aniqlash uchun barcha obyektlarni serializerga yuboramiz
        context = super().get_serializer_context()
        context['ranked_profiles'] = list(self.get_queryset())
        return context
    

@extend_schema(tags=['reting'])
class MonthlyRatingListView(ListAPIView):
    serializer_class = RatingSerializer
    pagination_class = RatingPagination

    def get_queryset(self):
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # joriy oyda berilgan ballarni yig‘amiz
        queryset = (
            Rating.objects.filter(created_at__gte=month_start)
            .values('user_profile')
            .annotate(score=Sum('point'))
            .order_by('-score')
        )

        # ID bo‘yicha Profile’larni olish
        profile_ids = [item['user_profile'] for item in queryset]
        profiles = list(Profile.objects.filter(id__in=profile_ids).select_related('user'))

        # Reytingni tartiblash uchun moslashtirish
        profiles_sorted = sorted(profiles, key=lambda p: next(q['score'] for q in queryset if q['user_profile'] == p.id), reverse=True)

        # score qiymatini vaqtinchalik o‘rnatamiz
        for p in profiles_sorted:
            p.score = next(q['score'] for q in queryset if q['user_profile'] == p.id)
        return profiles_sorted

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['ranked_profiles'] = self.get_queryset()
        return context



@extend_schema(tags=['reting'])
class StreakRatingListView(ListAPIView):
    serializer_class = RatingSerializer
    pagination_class = RatingPagination

    def get_queryset(self):
        profiles = Profile.objects.all().select_related('user')
        data = []

        for profile in profiles:
            streak = self.calculate_streak(profile)
            profile.score = streak  # score sifatida ketma-ket kunlar sonini ishlatamiz
            data.append(profile)

        data.sort(key=lambda p: p.score, reverse=True)
        return data

    def calculate_streak(self, profile):
        # foydalanuvchining barcha bajarilgan tasklari
        completions = CompleteTask.objects.filter(user=profile.user).order_by('-completed_at')
        if not completions.exists():
            return 0

        streak = 1
        prev_date = completions.first().completed_at.date()

        for comp in completions[1:]:
            current_date = comp.completed_at.date()
            diff = (prev_date - current_date).days
            if diff == 1:
                streak += 1
                prev_date = current_date
            elif diff > 1:
                break
        return streak

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['ranked_profiles'] = self.get_queryset()
        return context
