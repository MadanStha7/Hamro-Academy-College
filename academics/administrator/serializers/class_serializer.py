from rest_framework import serializers
from academics.models import (
    Class,
)
from .faculty import FacultySerializer
from .grade import GradeSerializer
from .section import SectionSerializer


class ClassSerializer(serializers.ModelSerializer):
    section = serializers.StringRelatedField(many=True, read_only=True)
    grade_name = serializers.CharField(source="grade.get_name_display", read_only=True)
    faculty_name = serializers.CharField(read_only=True)

    class Meta:
        model = Class
        read_only_fields = ["created_by", "institution"]
        fields = [
            "id",
            "section",
            "grade_name",
            "faculty_name",
            "created_by",
            "institution",
        ]

    # def create(self, validated_data):
    #     section = validated_data.pop("section")
    #     class_obj, created = Class.objects.update_or_create(
    #         grade=validated_data.get("grade"), defaults={**validated_data}
    #     )
    #     if section is not None:
    #         class_obj.section.set(section)
    #         class_obj.save()
    #     return class_obj
    #
    # def update(self, instance, validated_data):
    #     section = validated_data.pop("section")
    #     instance.grade = validated_data.get("grade", instance.grade)
    #     instance.section.set(section)
    #     instance.save()
    #     return instance
