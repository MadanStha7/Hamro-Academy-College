from academics.administrator.serializers.section import SectionSerializer
from rest_framework import serializers
from academics.models import Class, Section
from common.utils import validate_unique_faculty_grade


class ClassSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)

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

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res["section_data"] = SectionSerializer(instance.section.all(), many=True).data
        return res

    def validate(self, attrs):
        attrs = validate_unique_faculty_grade(
            Class, attrs, self.context.get("institution"), self.instance
        )
        return attrs
