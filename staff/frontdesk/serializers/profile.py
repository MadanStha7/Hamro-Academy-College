from rest_framework import serializers
from staff.administrator.serializers.document import DocumentSerializer
from staff.administrator.serializers.staff_academicinfo import (
    StaffAcademicInfoSerializer,
)
from staff.models import Staff
from user.common.serializers.user import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    """
    user profile serializer
    """

    user = UserSerializer(read_only=True)
    documents = DocumentSerializer(read_only=True, many=True)
    designation_display = serializers.CharField(
        source="designation.name", read_only=True
    )
    academic_info = StaffAcademicInfoSerializer(read_only=True)

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
            "academic_info",
            "documents",
        ]
