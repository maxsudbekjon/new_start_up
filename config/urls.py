
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path("chaining/", include("smart_selects.urls")),

    path('accounts/', include('accounts.urls')),
    path('task/', include('task.urls')),

    path("health/", health),

    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
from django.conf import settings
from django.urls import include, path

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns