from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers, status
from rest_framework.response import Response
from .serializers import CustomObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from user.administrator.serializers.user import UserSerializer
from core.serializers import InstitutionInfoSerializers


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data.pop("user")
            res = {
                "token": serializer.validated_data,
                "user_info": UserSerializer(user).data,
                "institution_info": InstitutionInfoSerializers(user.institution).data,
            }
            return Response(res)
        except TokenError as e:
            raise InvalidToken(e.args[0])
