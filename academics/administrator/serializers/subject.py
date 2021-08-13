from rest_framework import serializers

from academics.models import Subject
from common.utils import get_subject_type_name_of_value, validate_unique_name


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        read_only_fields = ["created_by", "institution"]
        fields = [
            "id",
            "name",
            "credit_hour",
            "subject_code",
            "subject_type",
            "is_optional",
            "created_by",
            "institution",
        ]

    def to_representation(self, data):
        data = super(SubjectSerializer, self).to_representation(data)
        data["subject_type"] = get_subject_type_name_of_value(data["subject_type"])
        return data

    def validate_name(self, name):
        name = validate_unique_name(
            Subject, name, self.context.get("institution"), self.instance
        )
        return name
