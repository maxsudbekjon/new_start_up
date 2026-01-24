from django.urls import path
from .views import MonthlyRatingListView, GlobalRatingListView, RegisterApiView, StreakRatingListView, UpdateUserProfileAPIView, UserDetailAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterApiView.as_view(),name='register'),
    path('login/', TokenObtainPairView.as_view(),name='login'),
    path('token/refresh/', TokenRefreshView.as_view(),name='token_refresh'),
    path('update_user_profile/', UpdateUserProfileAPIView.as_view(),name='update_user_profile'),
    path("user/detail/",UserDetailAPIView.as_view(),name='user_detail'),
    path('ratings/global/', GlobalRatingListView.as_view(),name='global_rating'),
    path('ratings/monthly/', MonthlyRatingListView.as_view(),name='monthly_rating'),
    path('ratings/streak/', StreakRatingListView.as_view(),name='streak_rating'),
]
