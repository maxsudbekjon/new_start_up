from django.urls import path
from .views import MonthlyRatingListView, GlobalRatingListView, RegisterApiView, StreakRatingListView, UpdateUserProfileAPIView, UserDetailAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('update_user_profile/', UpdateUserProfileAPIView.as_view()),
    path("user/detail",UserDetailAPIView.as_view()),
    path('ratings/global/', GlobalRatingListView.as_view()),
    path('ratings/monthly/', MonthlyRatingListView.as_view()),
    path('ratings/streak/', StreakRatingListView.as_view()),
]
