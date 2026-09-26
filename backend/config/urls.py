from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from history_ai.views_auth import (
    ChangePasswordView, PasswordResetConfirmView, PasswordResetRequestView, RegisterView,
)
from rest_framework.authtoken.views import obtain_auth_token

def health(request):
    """Monitoring uchun: server va baza ishlayaptimi."""
    from django.db import connection
    try:
        connection.ensure_connection()
    except Exception:
        return JsonResponse({'status': 'error'}, status=503)
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('api/health/', health, name='health'),
    path('admin/', admin.site.urls),
    path('api/auth/token/', obtain_auth_token, name='api-token-auth'),
    path('api/auth/register/', RegisterView.as_view(), name='api-register'),
    path('api/auth/password-reset/', PasswordResetRequestView.as_view(), name='api-password-reset'),
    path('api/auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='api-password-reset-confirm'),
    path('api/auth/change-password/', ChangePasswordView.as_view(), name='api-change-password'),
    path('api/history/', include('history_ai.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
