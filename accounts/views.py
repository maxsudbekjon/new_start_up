from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from accounts.models.profile import Profile
from drf_spectacular.utils import extend_schema

from accounts.serializers import CustomUserSerializer, ProfileSerializer
# from drf_spectacular.utils import
User = get_user_model()

@extend_schema(tags=["Auth"],request=CustomUserSerializer)
class RegisterApiView(APIView):
    permission_classes = [AllowAny]

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

@extend_schema(tags=["Auth"],request=ProfileSerializer)
class UpdateUserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user_profile = Profile.objects.get(user=request.user)

        serializer = ProfileSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


