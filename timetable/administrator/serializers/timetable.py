from rest_framework import serializers
from staff.models import Staff
from common.utils import validate_unique_name
from django.db import transaction
from django.contrib.auth import get_user_model
from timetable.models import TimeTable

User = get_user_model()


class TimeTableSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False, allow_null=True)
    section_name = serializers.CharField(source="section.name", read_only=True)
    grade_name = serializers.CharField(source="grade.name", read_only=True)

    teacher_full_name = serializers.CharField(
        source="teacher.user.get_full_name", read_only=True
    )
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    created_by = serializers.CharField(read_only=True)
    day_name = serializers.CharField(source="get_day_display", read_only=True)

    class Meta:
        model = TimeTable
        read_only_fields = ["academic_session", "section", "institution"]
        fields = [
            "id",
            "day",
            "day_name",
            "start_time",
            "end_time",
            "teacher",
            "subject",
            "academic_session",
            "grade_name",
            "teacher_full_name",
            "created_by",
            "subject_name",
            "section_name",
        ]

    def validate(self, data):
        if data["start_time"] >= data["end_time"]:
            raise serializers.ValidationError("start time must be before end time")

        return data


class TimetableListSerialzer(serializers.ModelSerializer):
    """
    serialzer to display list of timetable
    """

    subject__name = serializers.CharField(read_only=True)
    teacher__firstname = serializers.CharField(read_only=True)
    teacher__lastname = serializers.CharField(read_only=True)
    day_name = serializers.CharField(source="get_day_display", read_only=True)

    class Meta:
        model = TimeTable
        read_only_fields = ["academic_session", "section", "institution"]
        fields = [
            "id",
            "day_name",
            "start_time",
            "end_time",
            "academic_session",
            "subject__name",
            "teacher__firstname",
            "teacher__lastname",
            "teacher",
            "subject",
        ]


class TimeTableMultipleCreateSerializer(serializers.ModelSerializer):
    """
    serializer to create multiple timetable
    """

    days = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = TimeTable
        read_only_fields = [
            "academic_session",
            "section",
            "institution",
            "created_by",
            "teacher",
            "subject",
        ]
        fields = [
            "id",
            "day",
            "day_name",
            "start_time",
            "end_time",
            "teacher",
            "subject",
            "academic_session",
            "grade_name",
            "teacher_full_name",
            "created_by",
            "subject_name",
            "section_name",
        ]
