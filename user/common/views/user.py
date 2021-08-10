from user.common.serializers.user import UserSerializer, UserChangePasswordSerializer
from common.constant import SYSTEM_DEFAULT_PASSWORD
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

User = get_user_model()


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        object = self.request.user
        return object


class UserChangePasswordView(APIView):
    """
    api to change the user password
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, id=request.data.get("user"), institution=self.request.institution
        )
        old_password = self.request.data.get("old_password")
        if not user.check_password(old_password):
            raise ValidationError({"old_password": ["Old password is not correct"]})
        if old_password == self.request.data.get("password1"):
            raise ValidationError(
                {"error": ["you are not allowed to set the same old password"]}
            )
        if request.data.get("password1") == request.data.get("password2"):
            user.set_password(request.data.get("password1"))
            user.save()
            return Response({"message": ["password changed successfully"]})
        raise ValidationError({"error": [{"password": "password did not match"}]})
