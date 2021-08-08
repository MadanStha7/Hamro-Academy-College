from rest_framework import serializers

from common.utils import validate_unique_name
from student.models import StudentCategory


class StudentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCategory
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "name",
            "description"

        ]

    def validate_name(self, name):
        name = validate_unique_name(
            StudentCategory, name, self.context.get("institution"), self.instance
        )
        return name
