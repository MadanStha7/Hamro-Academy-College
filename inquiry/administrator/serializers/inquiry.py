from rest_framework import serializers
from inquiry.models import Inquiry
from common.utils import validate_unique_name
from common.utils import (
    return_grade_name_of_value,
    return_gender_value,
    return_marks_types_value,
    validate_unique_mobile_number,
    validate_unique_email,
)


class InquiryListSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(read_only=True)

    def to_representation(self, data):
        data = super(InquiryListSerializer, self).to_representation(data)
        data["gender"] = return_gender_value(data["gender"])
        data["marks_type"] = return_marks_types_value(data["marks_type"])
        return data

    class Meta:
        model = Inquiry
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "faculty",
            "contact_number",
            "previous_school",
            "marks_type",
            "marks_obtained",
            "remarks",
            "faculty_name",
            "email",
        ]
