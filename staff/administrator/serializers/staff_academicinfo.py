from rest_framework import serializers
from staff.models import StaffAcademicInfo
from django.db import transaction
from staff.administrator.serializers.department import DepartmentSerializer

# from common.utils import validate_unique_name


class StaffAcademicInfoSerializer(serializers.ModelSerializer):
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
            "department",
            "designation",
            "previous_academic_details",
            "previous_college_name",
            "full_address",
            "designation_name",
        ]

    def validate(self, attrs):
        # check if provided faculty is same or not
        no_of_department = []
        for item in attrs["department"]:
            no_of_department.append(item)

        for value in no_of_department:
            if no_of_department.count(value) > 1:
                raise serializers.ValidationError("Same Faculty cannot be selected!")

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        department_data = validated_data.pop("department")
        for department in department_data:
            department_id = department.id
        staff_academic = StaffAcademicInfo.objects.create(**validated_data)
        staff_academic.department.add(department_id)
        return staff_academic

    @transaction.atomic
    def update(self, instance, validated_data):
        department_data = validated_data.pop("department")
        for department in department_data:
            department_id = department.id
        super(StaffAcademicInfoSerializer, self).update(instance, validated_data)
        return instance
