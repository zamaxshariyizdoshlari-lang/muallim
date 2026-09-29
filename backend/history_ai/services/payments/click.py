"""Click Merchant (Shop-API) integratsiyasi - https://docs.click.uz/

Ikki bosqichli oqim: **Prepare** (action=0, to'lovdan oldin tekshirish) va **Complete**
(action=1, to'lov muvaffaqiyatli/muvaffaqiyatsiz yakunlangach). Ikkalasi ham shu bitta
webhook URL'ga form-encoded POST bilan keladi (JSON-RPC emas, oddiy maydonlar).

`merchant_trans_id` - bizning `Payment.id` (checkout havolasi yaratilganda oldindan
yaratiladi, Payme'dan farqli - u yerda tranzaksiyani Payme o'zi CreateTransaction bilan
yaratadi).
"""
import hashlib

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ...models import PAYMENT_GATEWAY_CLICK, PAYMENT_STATUS_CANCELLED, PAYMENT_STATUS_PAID, Payment
from . import extend_subscription, revoke_subscription_extension

ACTION_PREPARE = '0'
ACTION_COMPLETE = '1'

ERR_SUCCESS = 0
ERR_SIGN_FAILED = -1
ERR_INVALID_AMOUNT = -2
ERR_ACTION_NOT_FOUND = -3
ERR_ALREADY_PAID = -4
ERR_USER_NOT_FOUND = -5
ERR_TRANSACTION_NOT_FOUND = -6
ERR_BAD_REQUEST = -8
ERR_TRANSACTION_CANCELLED = -9


def _error(error_code, note, **extra):
    return JsonResponse({'error': error_code, 'error_note': note, **extra})


@method_decorator(csrf_exempt, name='dispatch')
class ClickMerchantView(View):
    def post(self, request):
        if not settings.CLICK_SECRET_KEY or not settings.CLICK_SERVICE_ID:
            return _error(ERR_BAD_REQUEST, "Xizmat sozlanmagan")

        p = request.POST
        required = ['click_trans_id', 'service_id', 'merchant_trans_id', 'amount', 'action', 'sign_time', 'sign_string']
        if any(k not in p for k in required):
            return _error(ERR_BAD_REQUEST, "Majburiy maydonlar yo'q")

        action = p.get('action')
        if action not in (ACTION_PREPARE, ACTION_COMPLETE):
            return _error(ERR_ACTION_NOT_FOUND, "Noto'g'ri action")

        if not self._check_sign(p, action):
            return _error(ERR_SIGN_FAILED, "Imzo noto'g'ri")

        try:
            payment = Payment.objects.get(pk=int(p['merchant_trans_id']), gateway=PAYMENT_GATEWAY_CLICK)
        except (Payment.DoesNotExist, ValueError):
            return _error(ERR_USER_NOT_FOUND, "Foydalanuvchi/buyurtma topilmadi")

        expected_amount = settings.SUBSCRIPTION_PRICE
        try:
            sent_amount = float(p['amount'])
        except ValueError:
            return _error(ERR_INVALID_AMOUNT, "Summa noto'g'ri")
        if abs(sent_amount - float(expected_amount)) > 0.01:
            return _error(ERR_INVALID_AMOUNT, "Summa mos emas")

        if action == ACTION_PREPARE:
            return self._prepare(payment, p)
        return self._complete(payment, p)

    def _check_sign(self, p, action):
        merchant_prepare_id = p.get('merchant_prepare_id', '')
        if action == ACTION_PREPARE:
            raw = (
                f"{p['click_trans_id']}{p['service_id']}{settings.CLICK_SECRET_KEY}"
                f"{p['merchant_trans_id']}{p['amount']}{p['action']}{p['sign_time']}"
            )
        else:
            raw = (
                f"{p['click_trans_id']}{p['service_id']}{settings.CLICK_SECRET_KEY}"
                f"{p['merchant_trans_id']}{merchant_prepare_id}{p['amount']}{p['action']}{p['sign_time']}"
            )
        expected = hashlib.md5(raw.encode('utf-8')).hexdigest()
        return expected == p.get('sign_string')

    def _prepare(self, payment, p):
        if payment.status == PAYMENT_STATUS_CANCELLED:
            return _error(ERR_TRANSACTION_CANCELLED, "Tranzaksiya bekor qilingan")
        if payment.status == PAYMENT_STATUS_PAID:
            return _error(ERR_ALREADY_PAID, "Allaqachon to'langan")

        payment.gateway_transaction_id = p['click_trans_id']
        payment.save(update_fields=['gateway_transaction_id'])
        return JsonResponse({
            'error': ERR_SUCCESS, 'error_note': 'Success',
            'click_trans_id': int(p['click_trans_id']), 'merchant_trans_id': p['merchant_trans_id'],
            'merchant_prepare_id': payment.id,
        })

    def _complete(self, payment, p):
        click_error = int(p.get('error') or 0)
        if click_error < 0:
            # Click tomonida to'lov muvaffaqiyatsiz tugagan (masalan foydalanuvchi bekor qilgan).
            if payment.status != PAYMENT_STATUS_PAID:
                payment.status = PAYMENT_STATUS_CANCELLED
                payment.cancelled_at = timezone.now()
                payment.save(update_fields=['status', 'cancelled_at'])
            return JsonResponse({
                'error': ERR_SUCCESS, 'error_note': 'Success',
                'click_trans_id': int(p['click_trans_id']), 'merchant_trans_id': p['merchant_trans_id'],
                'merchant_confirm_id': payment.id,
            })

        if payment.gateway_transaction_id != p['click_trans_id']:
            return _error(ERR_TRANSACTION_NOT_FOUND, "Tranzaksiya topilmadi")
        if str(p.get('merchant_prepare_id')) != str(payment.id):
            return _error(ERR_TRANSACTION_NOT_FOUND, "Tayyorlash ID mos emas")

        if payment.status != PAYMENT_STATUS_PAID:
            payment.status = PAYMENT_STATUS_PAID
            payment.paid_at = timezone.now()
            payment.save(update_fields=['status', 'paid_at'])
            extend_subscription(payment.user)

        return JsonResponse({
            'error': ERR_SUCCESS, 'error_note': 'Success',
            'click_trans_id': int(p['click_trans_id']), 'merchant_trans_id': p['merchant_trans_id'],
            'merchant_confirm_id': payment.id,
        })


def build_checkout_url(user):
    """Foydalanuvchini Click to'lov sahifasiga yo'naltirish uchun havola.

    Payme'dan farqli - bu yerda avval o'zimiz `Payment` yozuvini yaratamiz (pending, hali
    click_trans_id'siz), chunki Click Prepare so'rovida `merchant_trans_id` orqali shu
    yozuvni topishi kerak.
    """
    payment = Payment.objects.create(
        user=user, gateway=PAYMENT_GATEWAY_CLICK, amount=settings.SUBSCRIPTION_PRICE,
    )
    return (
        "https://my.click.uz/services/pay"
        f"?service_id={settings.CLICK_SERVICE_ID}"
        f"&merchant_id={settings.CLICK_MERCHANT_ID}"
        f"&amount={settings.SUBSCRIPTION_PRICE}"
        f"&transaction_param={payment.id}"
    )
