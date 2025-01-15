from django.contrib.auth.backends import BaseBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from customers.models import Customer
from partners.models import Partner

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        try:
            user = Customer.objects.get(username=username)
            if user.check_password(password):
                return user
        except Customer.DoesNotExist:
            pass

        try:
            user = Partner.objects.get(username=username)
            if user.check_password(password):
                return user
        except Partner.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            try:
                return Partner.objects.get(pk=user_id)
            except Partner.DoesNotExist:
                return None


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        user_type = validated_token.get('user_type')

        if not user_id or not user_type:
            return None

        if user_type == 'customer':
            try:
                return Customer.objects.get(pk=user_id)
            except Customer.DoesNotExist:
                return None
        elif user_type == 'partner':
            try:
                return Partner.objects.get(pk=user_id)
            except Partner.DoesNotExist:
                return None
        return None


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        if isinstance(user, Customer):
            token['user_type'] = 'customer'
        elif isinstance(user, Partner):
            token['user_type'] = 'partner'
        else:
            token['user_type'] = 'unknown'
        return token


class CustomToken:
    @staticmethod
    def generate_token(user):
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user)
        refresh['username'] = user.username

        if isinstance(user, Customer):
            refresh['user_type'] = 'customer'
        elif isinstance(user, Partner):
            refresh['user_type'] = 'partner'
        else:
            refresh['user_type'] = 'unknown'

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
