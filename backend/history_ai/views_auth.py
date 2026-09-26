from django.contrib.auth import get_user_model
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
    """Ochiq ro'yxatdan o'tish: istalgan odam login va parol bilan o'quvchi bo'la oladi."""

    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [RegisterThrottle]

    def post(self, request):
        User = get_user_model()
        username = (request.data.get('username') or '').strip()
        password = request.data.get('password') or ''
        first_name = (request.data.get('first_name') or '').strip()[:60]

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
        if errors:
            raise ValidationError(errors)

        user = User.objects.create_user(username=username, password=password, first_name=first_name)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
