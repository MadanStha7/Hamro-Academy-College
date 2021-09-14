from rest_framework import serializers
from staff.administrator.serializers.document import DocumentSerializer
from staff.administrator.serializers.staff_academicinfo import (
    StaffAcademicInfoSerializer,
)
from staff.administrator.serializers.staff import (
    StaffListSerializer,
)
from staff.models import Staff, StaffAcademicInfo, Document
from user.common.serializers.user import UserSerializer
from staff.administrator.serializers.department import DepartmentSerializer
from common.utils import (
    return_marital_status_value,
)


class StaffAcademicInfoProfileSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        res = super().to_representation(instance)
        res["department_name"] = DepartmentSerializer(
            instance.department.all(), many=True
        ).data
        return res

    designation_name = serializers.CharField(source="designation.name", read_only=True)

    class Meta:
        model = StaffAcademicInfo
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "staff",
            "designation",
            "previous_academic_details",
            "previous_college_name",
            "full_address",
            "designation_name",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    """
    user profile serializer
    """

    user = UserSerializer(read_only=True)
    designation_display = serializers.CharField(
        source="designation.name", read_only=True
    )
    staff_academic_info_details = StaffAcademicInfoProfileSerializer(read_only=True)

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
