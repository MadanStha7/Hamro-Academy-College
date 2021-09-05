from rest_framework import serializers
from inquiry.models import Inquiry
from common.utils import validate_unique_name
from common.utils import (
    return_grade_name_of_value,
    return_gender_value,
    return_marks_types_value,
    validate_unique_mobile_number,
    validate_Inquery_unique_email,
)


class InquirySerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(read_only=True)

    def to_representation(self, data):
        data = super(InquirySerializer, self).to_representation(data)
        data["gender_name"] = return_gender_value(data["gender"])
        data["marks_type_name"] = return_marks_types_value(data["marks_type"])
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

    def validate_contact_number(self, contact_number):
        """check that contact number is between 10 to 15 digits is already exist"""
        if len(contact_number) < 10 or len(contact_number) > 14:
            raise serializers.ValidationError("enter the correct phone number!")

        contact_number = validate_unique_mobile_number(
            Inquiry, contact_number, self.context.get("institution"), self.instance
        )
        return contact_number

    def validate_email(self, email):
        """check that email is already exist"""
        name = validate_Inquery_unique_email(
            Inquiry, email, self.context.get("institution"), self.instance
        )
        return name
