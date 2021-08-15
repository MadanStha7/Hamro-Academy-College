from rest_framework import serializers

from timetable.models import TimeTable


class TeacherTimeTableSerializer(serializers.ModelSerializer):
    """
    teacher api to view his timetable
    """

    day_name = serializers.CharField(read_only=True, source="get_day_display")
    grade_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)
    subject_name = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)
    shift_name = serializers.CharField(read_only=True)

    class Meta:
        model = TimeTable
        fields = [
            "id",
            "start_time",
            "end_time",
            "day_name",
            "grade_name",
            "section_name",
            "subject_name",
            "faculty_name",
            "shift_name"
        ]
