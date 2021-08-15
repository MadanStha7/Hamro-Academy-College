from rest_framework import serializers
from staff.models import StaffAcademicInfo
from django.db import transaction

# from common.utils import validate_unique_name


class StaffAcademicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAcademicInfo
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "staff",
            "shift",
            "faculty",
            "highest_degree",
            "experience",
            "working_days",
            "leave",
            "previous_academic_details",
            "previous_college_name",
            "previous_college_email",
            "previous_college_contact",
            "full_address",
        ]

    def validate(self, attrs):
        # check if provided faculty is same or not
        no_of_faculty = []
        for item in attrs["faculty"]:
            no_of_faculty.append(item)

        for value in no_of_faculty:
            if no_of_faculty.count(value) > 1:
                raise serializers.ValidationError("Same Faculty cannot be selected!")

        # check if provided shift is same or not
        no_of_shift = []
        for item in attrs["shift"]:
            no_of_shift.append(item)

        for value in no_of_shift:
            if no_of_shift.count(value) > 1:
                raise serializers.ValidationError("Same Shift cannot be selected!")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        faculty_data = validated_data.pop("faculty")
        shift_data = validated_data.pop("shift")
        for faculty in faculty_data:
            faculty_id = faculty.id
        for shift in shift_data:
            shift_id = shift.id
        staff_academic = StaffAcademicInfo.objects.create(**validated_data)
        staff_academic.faculty.add(faculty_id)
        staff_academic.shift.add(shift_id)
        return staff_academic

    @transaction.atomic
    def update(self, instance, validated_data):
        faculty_data = validated_data.pop("faculty")
        shift_data = validated_data.pop("shift")
        for faculty in faculty_data:
            instance.faculty.add(faculty)
        for shift in shift_data:
            instance.shift.add(shift)
        super(StaffAcademicInfoSerializer, self).update(instance, validated_data)
        return instance
