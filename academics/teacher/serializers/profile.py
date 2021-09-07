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
    documents = DocumentSerializer(read_only=True, many=True)
    designation_display = serializers.CharField(
        source="designation.name", read_only=True
    )

    def to_representation(self, instance):
        res = super().to_representation(instance)
        try:
            staff_academic_info = StaffAcademicInfo(staff=instance.id)
            res["staff_academic_info"] = StaffAcademicInfoSerializer(
                staff_academic_info
            ).data
        except StaffAcademicInfo.DoesNotExist:
            pass
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
            "documents",
        ]
