from rest_framework import serializers

from staff.models import Department
from common.utils import validate_unique_name


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serialzers to display data for department
    """

    faculty_name = serializers.ReadOnlyField(source="faculty.name")

    class Meta:
        model = Department
        read_only_fields = ["institution", "created_by"]
        fields = ["id", "name", "faculty", "faculty_name"]

    def validate_name(self, name):
        """check that designation is already exist"""
        name = validate_unique_name(
            Department, name, self.context.get("institution"), self.instance
        )
        return name
