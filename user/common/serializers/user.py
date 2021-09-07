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
            "middle_name",
            "email",
            "phone",
            "roles",
            "institution",
        )

    def validate_phone(self, value):
        if 10 > len(value) > 13:
            raise serializers.ValidationError(
                "length of phone number should be greater than or equal to 10 and less than or equal to 13"
            )
        return value


class UserChangePasswordSerializer(serializers.Serializer):
    user = serializers.UUIDField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    old_password = serializers.CharField(write_only=True)
