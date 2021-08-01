from rest_framework import serializers
from staff.models import Staff
from common.utils import validate_unique_name


class StaffSerializer(serializers.ModelSerializer):
    designation__name = serializers.CharField(read_only=True)
    faculty_name = serializers.StringRelatedField(
        many=True, read_only=True, source="faculty"
    )
    gender_name = serializers.CharField(source="get_gender_display", read_only=True)
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
            "user",
            "designation",
            "address",
            "phone",
            "dob",
            "gender",
            "religion",
            "blood_group",
            "pan_no",
            "date_of_joining",
            "designation__name",
            "gender_name",
            "religion_name",
            "blood_group_name",
            "faculty",
            "faculty_name",
        ]

    def validate(self, attrs):
        print("attrs", attrs)
        """
        check if the faculty is same
        """
        no_of_faculty = []
        for item in attrs["faculty"]:
            no_of_faculty.append(item)

        for value in no_of_faculty:
            if no_of_faculty.count(value) > 1:
                raise serializers.ValidationError("Same Faculty cannot be selected!")
        return attrs
