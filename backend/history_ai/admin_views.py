"""Admin panelning maxsus sahifalari (oddiy ModelAdmin bilan qilib bo'lmaydigan)."""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .services.admin_stats import platform_overview


@staff_member_required
def dashboard_view(request):
    from django.contrib import admin

    context = {
        **admin.site.each_context(request),
        'title': 'Platforma statistikasi',
        'stats': platform_overview(),
    }
    return render(request, 'admin/statistika.html', context)
