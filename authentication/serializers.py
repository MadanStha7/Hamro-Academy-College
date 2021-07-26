from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from common.constant import SYSTEM_DEFAULT_PASSWORD
from django.contrib.auth.models import update_last_login


class CustomObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if user.institution:
            token["institution"] = str(user.institution.id)

        roles = user.roles.all().values("title")
        token["roles"] = [role.get("title") for role in list(roles)]
        if user.check_password(SYSTEM_DEFAULT_PASSWORD):
            token["password_updated"] = False
        else:
            token["password_updated"] = True

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["password_updated"] = refresh["password_updated"]
        data["user"] = self.user
        data["access_expires_on"] = api_settings.ACCESS_TOKEN_LIFETIME
        data["refresh_expires_on"] = api_settings.REFRESH_TOKEN_LIFETIME
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data
