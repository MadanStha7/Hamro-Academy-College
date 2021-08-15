from rest_framework import serializers

from academics.helpers import validate_start_end_time, validate_date
from academics.models import OnlineClassInfo


class OnlineClassInfoSerializer(serializers.ModelSerializer):
    is_completed = serializers.BooleanField(read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)
    subject_name = serializers.CharField(read_only=True)
    teacher_first_name = serializers.CharField(read_only=True)
    teacher_last_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)
    grade_name = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)
    class_date = serializers.CharField(required=True)

    class Meta:
        model = OnlineClassInfo
        fields = [
            "id",
            "subject",
            "teacher_first_name",
            "teacher_last_name",
            "subject_name",
            "class_date",
            "start_time",
            "end_time",
            "grade",
            "grade_name",
            "section",
            "section_name",
            "faculty",
            "faculty_name",
            "link_code",
            "is_completed",
            "is_upcoming",
            "is_ongoing",
        ]

    def validate(self, value):
        validate_start_end_time(value)
        return super(OnlineClassInfoSerializer, self).validate(value)

    def validate_class_date(self, value):
        value = validate_date(value)
        return value

