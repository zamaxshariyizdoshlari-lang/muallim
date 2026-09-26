from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from history_ai.views_auth import (
    ChangePasswordView, PasswordResetConfirmView, PasswordResetRequestView, RegisterView,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
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
