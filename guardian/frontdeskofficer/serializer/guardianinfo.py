from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers
from common.utils import validate_unique_phone, to_internal_value
from guardian.models import StudentGuardianInfo
from staff.administrator.serializers.staff import UserSerializer

User = get_user_model()


class GuardianInfoSerializer(serializers.ModelSerializer):
    guardian_first_name = serializers.CharField(read_only=True)
    guardian_last_name = serializers.CharField(read_only=True)
    guardian_phone_number = serializers.CharField(read_only=True)
    guardian_email = serializers.CharField(read_only=True)
    photo = serializers.SerializerMethodField(
        read_only=True, required=False, allow_null=True
    )

    def get_photo(self, obj):
        return obj.photo.url if obj.photo else None

    class Meta:
        model = StudentGuardianInfo
        read_only_fields = ["photo", "institution", "created_by"]
        fields = [
            "id",
            "address",
            "relation",
            "photo",
            "phone",
            "occupation",
            "institution",
            "created_by",
            "guardian_first_name",
            "guardian_last_name",
            "guardian_phone_number",
            "guardian_email",
        ]
