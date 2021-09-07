from rest_framework import serializers
from staff.models import Staff
from common.utils import validate_unique_phone, validate_unique_email
from academics.models import Faculty, Grade
from common.utils import to_internal_value
from django.db import transaction
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


class StaffListSerializer(serializers.ModelSerializer):
    designation_name = serializers.CharField(read_only=True)
    staff_contact_number = serializers.CharField(read_only=True)
    staff_email = serializers.CharField(read_only=True)
    staff_first_name = serializers.CharField(read_only=True)
    staff_middle_name = serializers.CharField(read_only=True)
    staff_last_name = serializers.CharField(read_only=True)
    gender_name = serializers.CharField(source="get_gender_display", read_only=True)
    religion_name = serializers.CharField(source="get_religion_display", read_only=True)
    blood_group_name = serializers.CharField(
        source="get_blood_group_display", read_only=True
    )

    class Meta:
        model = Staff
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "photo",
            "address",
            "blood_group_name",
            "religion_name",
            "designation_name",
            "gender_name",
            "staff_contact_number",
            "staff_email",
            "staff_first_name",
            "staff_middle_name",
            "staff_last_name",
        ]
