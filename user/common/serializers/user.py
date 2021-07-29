from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .role import RoleSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        read_only_fields = ["institution"]
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "roles",
            "institution",
        )
