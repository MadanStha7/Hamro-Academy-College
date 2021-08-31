from rest_framework import serializers
from timetable.models import TimeTable


class StudentTeacherSerializer(serializers.ModelSerializer):
    teacher_full_name = serializers.CharField(read_only=True)
    subject_name = serializers.CharField(read_only=True)

    class Meta:
        model = TimeTable
        fields = [
            "teacher",
            "teacher_full_name",
            "subject",
            "subject_name",
        ]
