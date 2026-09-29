import glob
import json
import traceback

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
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


@staff_member_required
def reimport_debug(request):
    """Vaqtinchalik diagnostika: barcha content/*/book.json fayllarini shu (production) muhitda,
    shu (production) bazaga qarshi qayta import qilib, har birining natijasi yoki to'liq xato
    matnini (traceback) brauzerda oddiy matn sifatida ko'rsatadi.

    Build logini Render Dashboard'da qidirish o'rniga - admin sifatida tizimga kirgan holda shu
    URL'ni ochish kifoya. Faqat is_staff foydalanuvchilar kira oladi.
    """
    from history_ai.services.book_import import import_book_json

    lines = []
    pattern = str(settings.BASE_DIR / 'content' / '*' / 'book.json')
    paths = sorted(glob.glob(pattern))
    lines.append(f"Qidirilgan yo'l: {pattern}")
    lines.append(f"Topilgan fayllar: {len(paths)}")
    lines.append('')
    for path in paths:
        lines.append(f"=== {path} ===")
        try:
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
            result = import_book_json(data, request.user)
            lines.append(f"OK: {result}")
        except Exception:
            lines.append(traceback.format_exc())
        lines.append('')
    return HttpResponse('\n'.join(lines), content_type='text/plain; charset=utf-8')


urlpatterns = [
    path('api/health/', health, name='health'),
    path('admin/reimport-debug/', reimport_debug, name='reimport-debug'),
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
