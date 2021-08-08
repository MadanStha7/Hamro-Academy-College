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
        faculty_obj = self.instance.faculty
        shift_obj = self.instance.shift
        instance.staff = validated_data.get("staff", instance.staff)
        instance.highest_degree = validated_data.get(
            "highest_degree", instance.highest_degree
        )
        instance.experience = validated_data.get("experience", instance.experience)
        instance.working_days = validated_data.get(
            "working_days", instance.working_days
        )
        instance.leave = validated_data.get("leave", instance.leave)
        instance.previous_academic_details = validated_data.get(
            "previous_academic_details", instance.previous_academic_details
        )
        instance.previous_college_name = validated_data.get(
            "previous_college_name", instance.previous_college_name
        )
        instance.full_address = validated_data.get(
            "full_address", instance.full_address
        )

        for faculty in faculty_data:
            instance.faculty.add(faculty)
        for shift in shift_data:
            instance.shift.add(shift)
        return instance
