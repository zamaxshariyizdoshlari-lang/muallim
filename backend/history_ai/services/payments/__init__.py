"""Payme va Click orqali oylik obuna to'lovlari.

Umumiy oqim: foydalanuvchi "checkout" havolasini oladi (payme.py/click.py'dagi
`build_checkout_url`), to'lov tizimi saytida to'laydi, so'ng tizim bizning webhook
endpoint'imizga (PaymeMerchantView / ClickMerchantView) murojaat qilib, to'lovni
tasdiqlaydi - shunda `extend_subscription` chaqiriladi.
"""
from django.utils import timezone


def extend_subscription(user, days=30):
    """Obunani uzaytiradi: agar hali faol bo'lsa muddatidan, aks holda hozirdan boshlab."""
    from ...models import Subscription

    sub, _ = Subscription.objects.get_or_create(user=user)
    now = timezone.now()
    base = sub.current_period_end if sub.current_period_end and sub.current_period_end > now else now
    sub.current_period_end = base + timezone.timedelta(days=days)
    sub.save(update_fields=['current_period_end', 'updated_at'])
    return sub


def revoke_subscription_extension(user, days=30):
    """To'lov bekor qilinganda (masalan qaytarib berilganda) obunani orqaga qaytaradi."""
    from ...models import Subscription

    sub = getattr(user, 'subscription', None)
    if not sub or not sub.current_period_end:
        return
    sub.current_period_end = sub.current_period_end - timezone.timedelta(days=days)
    sub.save(update_fields=['current_period_end', 'updated_at'])
