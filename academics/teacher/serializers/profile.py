from rest_framework import serializers

from staff.administrator.serializers.document import DocumentSerializer
from staff.administrator.serializers.staff_academicinfo import (
    StaffAcademicInfoSerializer,
)
from staff.models import Staff, StaffAcademicInfo
from user.common.serializers.user import UserSerializer
from common.utils import (
    return_marital_status_value,
)


class ProfileSerializer(serializers.ModelSerializer):
    """
    user profile serializer
    """

    user = UserSerializer(read_only=True)
    designation_display = serializers.CharField(
        source="designation.name", read_only=True
    )
    staff_academic_info_details = StaffAcademicInfoSerializer(read_only=True)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res["marital_status"] = return_marital_status_value(res["marital_status"])
        return res

    class Meta:
        model = Staff
        read_only_fields = ["photo"]
        fields = [
            "id",
            "photo",
            "user",
            "designation",
            "designation_display",
            "address",
            "dob",
            "marital_status",
            "staff_academic_info_details",
        ]
