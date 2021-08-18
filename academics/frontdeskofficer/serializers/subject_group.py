from rest_framework import serializers
from academics.administrator.serializers.section import SectionSerializer
from academics.administrator.serializers.subject import SubjectSerializer
from academics.models import SubjectGroup, Subject, Section
from common.utils import return_grade_name_of_value, validate_unique_name


class SubjectGroupSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)

    class Meta:
        model = SubjectGroup
        read_only_fields = ["created_by", "institution"]
        fields = [
            "id",
            "name",
            "subject",
            "section",
            "description",
            "created_by",
            "institution",
            "grade_name",
            "faculty_name",
        ]

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res["subject"] = SectionSerializer(
            instance.subject.all().values("name"), many=True
        ).data
        res["section"] = SectionSerializer(
            instance.section.all().values("name"), many=True
        ).data
        return res
