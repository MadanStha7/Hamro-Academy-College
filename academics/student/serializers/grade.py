from rest_framework import serializers
from timetable.models import TimeTable


class StudentGradeTimetableSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)
    subject_name = serializers.CharField(read_only=True)
    subject_credit_hour = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )
    subject_type = serializers.CharField(read_only=True)
    teacher_full_name = serializers.CharField(
        source="teacher.user.get_full_name", read_only=True
    )
    day_name = serializers.CharField(source="get_day_display", read_only=True)

    class Meta:
        model = TimeTable
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
            "faculty_name",
            "teacher_full_name",
            "created_by",
            "subject_name",
            "subject_credit_hour",
            "subject_type",
            "section_name",
        ]
