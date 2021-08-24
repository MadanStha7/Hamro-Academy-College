from rest_framework import serializers
from staff.models import Staff
from django.db import transaction
from django.contrib.auth import get_user_model
from timetable.models import TimeTable

User = get_user_model()


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
