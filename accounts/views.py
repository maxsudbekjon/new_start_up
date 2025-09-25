from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer, ProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample
from accounts.models.profile import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterApiView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Yangi foydalanuvchi ro‘yxatdan o‘tkazish",
        description="Yangi foydalanuvchi yaratish uchun kerakli ma’lumotlarni yuboring.",
        request=CustomUserSerializer,
        responses={201: CustomUserSerializer, 400: dict},
        examples=[
            OpenApiExample(
                "Register Example",
                value={
                    "username": "ali123",
                    "age": 20,
                    "phone": "+998901234567",
                    "password": "strong_password",
                    "password2": "strong_password"
                },
                request_only=True,
            ),
            OpenApiExample(
                "Register Success Response",
                value={
                    "id": 1,
                    "username": "ali123",
                    "age": 20,
                    "phone": "+998901234567"
                },
                response_only=True,
            )
        ]
    )
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['phone'] = user.phone
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        summary="Login qilish (JWT olish)",
        description="Foydalanuvchi username/phone va parol bilan login qiladi va access/refresh token oladi.",
        request=TokenObtainPairSerializer,
        responses={200: dict, 401: dict},
        examples=[
            OpenApiExample(
                "Login Example",
                value={
                    "username": "ali123",
                    "password": "strong_password",
                    "phone": "+998901234567"
                },
                request_only=True,
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UpdateUserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Foydalanuvchi profilini yangilash",
        description="Foydalanuvchi faqat o‘z profilini qisman (PATCH) yangilashi mumkin.",
        request=ProfileSerializer,
        responses={200: ProfileSerializer, 400: dict, 404: dict},
        examples=[
            OpenApiExample(
                "Profile Update Example",
                value={
                    "first_name": "Ali",
                    "last_name": "Valiyev",
                    "bio": "Men dasturchiman"
                },
                request_only=True,
            )
        ]
    )
    def patch(self, request):
        user_profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class GetUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "user profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=200)



