from rest_framework import serializers

from onlineclass.administrator.utils.helpers import validate_date
from onlineclass.models import OnlineClassInfo


class OnlineClassSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)
    subject_name = serializers.CharField(read_only=True)

    class Meta:
        model = OnlineClassInfo
        read_only_fields = ["created_by", "academic_session", "institution"]
        fields = [
            "id",
            "title",
            "subject",
            "subject_name",
            "class_date",
            "days",
            "start_time",
            "end_time",
            "grade",
            "grade_name",
            "section",
            "section_name",
            "faculty",
            "faculty_name",
            "link_code",
            "is_regular",
        ]

    def validate(self, data):
        if data["start_time"] > data["end_time"]:
            raise serializers.ValidationError("start time must be before end time")
        return data

    def validate_class_date(self, value):
        if value:
            value = validate_date(value)
        return value
