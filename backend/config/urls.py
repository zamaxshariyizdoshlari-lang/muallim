from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from history_ai.views_auth import RegisterView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', obtain_auth_token, name='api-token-auth'),
    path('api/auth/register/', RegisterView.as_view(), name='api-register'),
    path('api/history/', include('history_ai.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
