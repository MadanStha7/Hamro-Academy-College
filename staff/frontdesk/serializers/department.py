from rest_framework import serializers
from staff.models import Department


class DepartmentListSerializer(serializers.ModelSerializer):
    """
    Serialzers to display data for department
    """

    faculty_name = serializers.ReadOnlyField(source="faculty.name")

    class Meta:
        model = Department
        read_only_fields = ["institution", "created_by"]
        fields = ["id", "name", "faculty", "faculty_name"]
