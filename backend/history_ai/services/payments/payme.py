"""Payme Merchant API (JSON-RPC 2.0) - https://developer.help.paycom.uz/

Payme checkout.paycom.uz orqali to'lov qabul qilgach, shu endpoint'ga (bitta URL, barcha
metodlar `method` maydoni orqali) so'rov yuboradi. Summalar TIYIN'da (so'm * 100).
"""
import base64
import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ...models import (
    PAYMENT_GATEWAY_PAYME, PAYMENT_STATUS_CANCELLED, PAYMENT_STATUS_PAID, PAYMENT_STATUS_PENDING,
    Payment,
)
from . import extend_subscription, revoke_subscription_extension

User = get_user_model()

STATE_PENDING = 1
STATE_PAID = 2
STATE_CANCELLED_PENDING = -1
STATE_CANCELLED_PAID = -2

ERR_INVALID_AMOUNT = -31001
ERR_ACCOUNT_NOT_FOUND = -31050
ERR_TRANSACTION_NOT_FOUND = -31003
ERR_CANNOT_PERFORM = -31006
ERR_CANNOT_CANCEL = -31007
ERR_ALREADY_PERFORMED = -31008
ERR_ALREADY_CANCELLED = -31009
ERR_INSUFFICIENT_PRIVILEGE = -32504
ERR_METHOD_NOT_FOUND = -32601


def _err(msg_uz, msg_ru, msg_en, code, data=None):
    error = {'code': code, 'message': {'uz': msg_uz, 'ru': msg_ru, 'en': msg_en}}
    if data:
        error['data'] = data
    return error


def _ms(dt):
    if not dt:
        return 0
    return int(dt.timestamp() * 1000)


def _payment_state(payment):
    if payment.status == PAYMENT_STATUS_PAID:
        return STATE_PAID
    if payment.status == PAYMENT_STATUS_CANCELLED:
        return STATE_CANCELLED_PAID if payment.paid_at else STATE_CANCELLED_PENDING
    return STATE_PENDING


@method_decorator(csrf_exempt, name='dispatch')
class PaymeMerchantView(View):
    """Bitta URL - barcha Payme metodlari shu yerga JSON-RPC orqali keladi."""

    def post(self, request):
        if not settings.PAYME_MERCHANT_ID or not settings.PAYME_SECRET_KEY:
            return JsonResponse({'error': _err(
                "Xizmat sozlanmagan", "Сервис не настроен", "Service not configured", ERR_INSUFFICIENT_PRIVILEGE,
            )}, status=200)

        auth_error = self._check_auth(request)
        if auth_error:
            return JsonResponse({'error': auth_error})

        try:
            body = json.loads(request.body or b'{}')
        except ValueError:
            return JsonResponse({'error': _err(
                "Noto'g'ri so'rov", "Неверный запрос", "Invalid request", -32700,
            )})

        rpc_id = body.get('id')
        method = body.get('method')
        params = body.get('params') or {}

        handler = {
            'CheckPerformTransaction': self.check_perform_transaction,
            'CreateTransaction': self.create_transaction,
            'PerformTransaction': self.perform_transaction,
            'CancelTransaction': self.cancel_transaction,
            'CheckTransaction': self.check_transaction,
            'GetStatement': self.get_statement,
        }.get(method)

        if not handler:
            return JsonResponse({'jsonrpc': '2.0', 'id': rpc_id, 'error': _err(
                "Noma'lum metod", "Неизвестный метод", "Unknown method", ERR_METHOD_NOT_FOUND,
            )})

        result_or_error = handler(params)
        if 'error' in result_or_error:
            return JsonResponse({'jsonrpc': '2.0', 'id': rpc_id, 'error': result_or_error['error']})
        return JsonResponse({'jsonrpc': '2.0', 'id': rpc_id, 'result': result_or_error['result']})

    def _check_auth(self, request):
        header = request.META.get('HTTP_AUTHORIZATION', '')
        if not header.startswith('Basic '):
            return _err("Ruxsat yo'q", "Доступ запрещен", "Access denied", ERR_INSUFFICIENT_PRIVILEGE)
        try:
            decoded = base64.b64decode(header[len('Basic '):]).decode('utf-8')
            login, _, key = decoded.partition(':')
        except Exception:
            return _err("Ruxsat yo'q", "Доступ запрещен", "Access denied", ERR_INSUFFICIENT_PRIVILEGE)
        if login != 'Paycom' or key != settings.PAYME_SECRET_KEY:
            return _err("Ruxsat yo'q", "Доступ запрещен", "Access denied", ERR_INSUFFICIENT_PRIVILEGE)
        return None

    def _resolve_account(self, account):
        user_id = account.get('user_id')
        if not user_id:
            return None
        try:
            return User.objects.get(pk=int(user_id), is_active=True)
        except (User.DoesNotExist, ValueError, TypeError):
            return None

    def _expected_amount(self):
        return settings.SUBSCRIPTION_PRICE * 100

    def check_perform_transaction(self, params):
        user = self._resolve_account(params.get('account') or {})
        if not user:
            return {'error': _err(
                "Foydalanuvchi topilmadi", "Пользователь не найден", "User not found",
                ERR_ACCOUNT_NOT_FOUND, data='user_id',
            )}
        if params.get('amount') != self._expected_amount():
            return {'error': _err(
                "Summa noto'g'ri", "Неверная сумма", "Invalid amount", ERR_INVALID_AMOUNT,
            )}
        return {'result': {'allow': True}}

    def create_transaction(self, params):
        payme_id = params.get('id')
        user = self._resolve_account(params.get('account') or {})
        if not user:
            return {'error': _err(
                "Foydalanuvchi topilmadi", "Пользователь не найден", "User not found",
                ERR_ACCOUNT_NOT_FOUND, data='user_id',
            )}
        if params.get('amount') != self._expected_amount():
            return {'error': _err(
                "Summa noto'g'ri", "Неверная сумма", "Invalid amount", ERR_INVALID_AMOUNT,
            )}

        existing = Payment.objects.filter(
            gateway=PAYMENT_GATEWAY_PAYME, gateway_transaction_id=payme_id,
        ).first()
        if existing:
            if existing.status == PAYMENT_STATUS_CANCELLED:
                return {'error': _err(
                    "Tranzaksiya bekor qilingan", "Транзакция отменена", "Transaction cancelled",
                    ERR_CANNOT_PERFORM,
                )}
            return {'result': {
                'create_time': _ms(existing.created_at), 'transaction': str(existing.id),
                'state': _payment_state(existing),
            }}

        # Payme bitta buyurtma uchun bir vaqtda faqat bitta faol (pending) tranzaksiya kutadi.
        other_pending = Payment.objects.filter(
            user=user, gateway=PAYMENT_GATEWAY_PAYME, status=PAYMENT_STATUS_PENDING,
        ).exclude(gateway_transaction_id=payme_id).exists()
        if other_pending:
            return {'error': _err(
                "Boshqa tranzaksiya kutilmoqda", "Ожидается другая транзакция",
                "Another transaction is pending", ERR_CANNOT_PERFORM,
            )}

        payment = Payment.objects.create(
            user=user, gateway=PAYMENT_GATEWAY_PAYME, gateway_transaction_id=payme_id,
            amount=settings.SUBSCRIPTION_PRICE, status=PAYMENT_STATUS_PENDING,
        )
        return {'result': {
            'create_time': _ms(payment.created_at), 'transaction': str(payment.id),
            'state': STATE_PENDING,
        }}

    def perform_transaction(self, params):
        payment = Payment.objects.filter(
            gateway=PAYMENT_GATEWAY_PAYME, gateway_transaction_id=params.get('id'),
        ).first()
        if not payment:
            return {'error': _err(
                "Tranzaksiya topilmadi", "Транзакция не найдена", "Transaction not found",
                ERR_TRANSACTION_NOT_FOUND,
            )}
        if payment.status == PAYMENT_STATUS_CANCELLED:
            return {'error': _err(
                "Tranzaksiya bekor qilingan", "Транзакция отменена", "Transaction cancelled",
                ERR_CANNOT_PERFORM,
            )}
        if payment.status == PAYMENT_STATUS_PAID:
            return {'result': {
                'transaction': str(payment.id), 'perform_time': _ms(payment.paid_at), 'state': STATE_PAID,
            }}

        payment.status = PAYMENT_STATUS_PAID
        payment.paid_at = timezone.now()
        payment.save(update_fields=['status', 'paid_at'])
        extend_subscription(payment.user)
        return {'result': {
            'transaction': str(payment.id), 'perform_time': _ms(payment.paid_at), 'state': STATE_PAID,
        }}

    def cancel_transaction(self, params):
        payment = Payment.objects.filter(
            gateway=PAYMENT_GATEWAY_PAYME, gateway_transaction_id=params.get('id'),
        ).first()
        if not payment:
            return {'error': _err(
                "Tranzaksiya topilmadi", "Транзакция не найдена", "Transaction not found",
                ERR_TRANSACTION_NOT_FOUND,
            )}
        was_paid = payment.status == PAYMENT_STATUS_PAID
        if payment.status != PAYMENT_STATUS_CANCELLED:
            payment.status = PAYMENT_STATUS_CANCELLED
            payment.cancelled_at = timezone.now()
            payment.save(update_fields=['status', 'cancelled_at'])
            if was_paid:
                revoke_subscription_extension(payment.user)
        return {'result': {
            'transaction': str(payment.id), 'cancel_time': _ms(payment.cancelled_at),
            'state': STATE_CANCELLED_PAID if was_paid else STATE_CANCELLED_PENDING,
        }}

    def check_transaction(self, params):
        payment = Payment.objects.filter(
            gateway=PAYMENT_GATEWAY_PAYME, gateway_transaction_id=params.get('id'),
        ).first()
        if not payment:
            return {'error': _err(
                "Tranzaksiya topilmadi", "Транзакция не найдена", "Transaction not found",
                ERR_TRANSACTION_NOT_FOUND,
            )}
        return {'result': {
            'create_time': _ms(payment.created_at),
            'perform_time': _ms(payment.paid_at),
            'cancel_time': _ms(payment.cancelled_at),
            'transaction': str(payment.id),
            'state': _payment_state(payment),
            'reason': None,
        }}

    def get_statement(self, params):
        from_dt = timezone.datetime.fromtimestamp((params.get('from') or 0) / 1000, tz=timezone.get_current_timezone())
        to_dt = timezone.datetime.fromtimestamp((params.get('to') or 0) / 1000, tz=timezone.get_current_timezone())
        payments = Payment.objects.filter(
            gateway=PAYMENT_GATEWAY_PAYME, created_at__gte=from_dt, created_at__lte=to_dt,
        )
        return {'result': {'transactions': [
            {
                'id': p.gateway_transaction_id, 'time': _ms(p.created_at),
                'amount': int(p.amount) * 100, 'account': {'user_id': str(p.user_id)},
                'create_time': _ms(p.created_at), 'perform_time': _ms(p.paid_at),
                'cancel_time': _ms(p.cancelled_at), 'transaction': str(p.id),
                'state': _payment_state(p), 'reason': None,
            }
            for p in payments
        ]}}


def build_checkout_url(user):
    """Foydalanuvchini Payme to'lov sahifasiga yo'naltirish uchun havola."""
    params = f"m={settings.PAYME_MERCHANT_ID};ac.user_id={user.id};a={settings.SUBSCRIPTION_PRICE * 100}"
    encoded = base64.b64encode(params.encode('utf-8')).decode('utf-8')
    host = 'test.paycom.uz' if settings.PAYME_TEST_MODE else 'checkout.paycom.uz'
    return f"https://{host}/{encoded}"
