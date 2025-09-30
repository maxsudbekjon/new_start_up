from django.urls import path

from .views import RegisterApiView, CustomTokenObtainPairView, UpdateUserProfileAPIView, GetUserProfile

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # profile
    path('update_user_profile/', UpdateUserProfileAPIView.as_view(), ),
    path('get_my_pofile/', GetUserProfile.as_view(), ),

]
