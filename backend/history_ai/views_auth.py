from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView


class RegisterThrottle(AnonRateThrottle):
    scope = 'register'


class RegisterView(APIView):
    """Ochiq ro'yxatdan o'tish: istalgan odam login va parol bilan talaba bo'la oladi."""

    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [RegisterThrottle]

    def post(self, request):
        User = get_user_model()
        username = (request.data.get('username') or '').strip()
        password = request.data.get('password') or ''
        first_name = (request.data.get('first_name') or '').strip()[:60]
        email = (request.data.get('email') or '').strip().lower()

        errors = {}
        if len(username) < 3 or len(username) > 30 or not username.replace('_', '').replace('.', '').isalnum():
            errors['username'] = "Login 3-30 belgi: harf, raqam, nuqta yoki pastki chiziq."
        elif User.objects.filter(username__iexact=username).exists():
            errors['username'] = "Bu login band."
        if len(password) < 8:
            errors['password'] = "Parol kamida 8 belgidan iborat bo'lsin."
        elif password.isdigit():
            errors['password'] = "Parol faqat raqamlardan iborat bo'lmasin."
        elif password.lower() == username.lower():
            errors['password'] = "Parol loginga o'xshash bo'lmasin."
        if email:
            try:
                validate_email(email)
            except DjangoValidationError:
                errors['email'] = "Email manzili noto'g'ri."
            else:
                if User.objects.filter(email__iexact=email).exists():
                    errors['email'] = "Bu email bilan hisob mavjud."
        if errors:
            raise ValidationError(errors)

        user = User.objects.create_user(username=username, password=password, first_name=first_name, email=email)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


def _check_password(password, username=''):
    if len(password) < 8:
        return "Parol kamida 8 belgidan iborat bo'lsin."
    if password.isdigit():
        return "Parol faqat raqamlardan iborat bo'lmasin."
    if username and password.lower() == username.lower():
        return "Parol loginga o'xshash bo'lmasin."
    return None


class PasswordResetThrottle(AnonRateThrottle):
    scope = 'password_reset'


class PasswordResetRequestView(APIView):
    """Parolni tiklash havolasini emailga yuboradi. Email mavjudligini oshkor qilmaydi."""

    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [PasswordResetThrottle]

    def post(self, request):
        User = get_user_model()
        email = (request.data.get('email') or '').strip().lower()
        if email:
            for user in User.objects.filter(email__iexact=email, is_active=True)[:3]:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                link = f"{settings.FRONTEND_URL}/parolni-tiklash?uid={uid}&token={token}"
                send_mail(
                    "Muallim: parolni tiklash",
                    f"Salom, {user.first_name or user.username}!\n\nParolni tiklash uchun havola:\n{link}\n\n"
                    "Agar bu so'rovni siz yubormagan bo'lsangiz, xatni e'tiborsiz qoldiring.",
                    settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True,
                )
        return Response({'detail': "Agar bu email ro'yxatdan o'tgan bo'lsa, tiklash havolasi yuborildi."})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [PasswordResetThrottle]

    def post(self, request):
        User = get_user_model()
        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(request.data.get('uid') or '')))
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise ValidationError({'detail': "Havola yaroqsiz."})
        if not default_token_generator.check_token(user, request.data.get('token') or ''):
            raise ValidationError({'detail': "Havola eskirgan yoki yaroqsiz. Qaytadan so'rang."})
        password = request.data.get('password') or ''
        err = _check_password(password, user.username)
        if err:
            raise ValidationError({'password': err})
        user.set_password(password)
        user.save()
        Token.objects.filter(user=user).delete()
        return Response({'detail': "Parol yangilandi. Endi kirishingiz mumkin."})


class ChangePasswordView(APIView):
    def post(self, request):
        user = request.user
        if not user.check_password(request.data.get('old_password') or ''):
            raise ValidationError({'old_password': "Joriy parol noto'g'ri."})
        new = request.data.get('new_password') or ''
        err = _check_password(new, user.username)
        if err:
            raise ValidationError({'new_password': err})
        user.set_password(new)
        user.save()
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return Response({'token': token.key})
