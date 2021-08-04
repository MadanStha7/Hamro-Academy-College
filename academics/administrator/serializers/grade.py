from rest_framework import serializers
from academics.models import Grade
from common.utils import return_grade_name_of_value, validate_unique_name


class GradeSerializer(serializers.ModelSerializer):
    def to_representation(self, data):
        data = super(GradeSerializer, self).to_representation(data)
        data["name"] = return_grade_name_of_value(data["name"])
        return data

    class Meta:
        model = Grade
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "name",
            "created_by",
            "institution",
        ]

    def validate_name(self, name):
        name = validate_unique_name(
            Grade, name, self.context.get("institution"), self.instance
        )
        return name
