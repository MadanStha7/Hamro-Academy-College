from rest_framework import serializers
from academics.models import (
    Faculty,
    Shift,
)
from common.utils import validate_unique_name
from .faculty import FacultySerializer


class ShiftSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(read_only=True)

    class Meta:
        model = Shift
        read_only_fields = ["created_by", "institution"]
        fields = [
            "id",
            "name",
            "start_time",
            "end_time",
            "faculty_name",
            "faculty",
            "created_by",
            "institution",
        ]

    def validate_name(self, name):
        name = validate_unique_name(
            Shift, name, self.context.get("institution"), self.instance
        )
        return name

    def validate(self, data):
        if data["start_time"] > data["end_time"]:
            raise serializers.ValidationError("start time must be before end time")
        return data
