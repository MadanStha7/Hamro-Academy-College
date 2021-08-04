from rest_framework import serializers
from academics.models import Class
from common.utils import validate_unique_faculty_grade


class ClassSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = Class
        read_only_fields = ["created_by", "institution"]
        fields = [
            "id",
            "section",
            "grade",
            "grade_name",
            "faculty",
            "faculty_name",
            "created_by",
            "institution",
        ]

    def validate(self, attrs):
        attrs = validate_unique_faculty_grade(
            Class, attrs, self.context.get("institution"), self.instance
        )
        return attrs
