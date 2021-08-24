from rest_framework import serializers
from timetable.models import TimeTable


class StudentTeacherSerializer(serializers.ModelSerializer):
    teacher_first_name = serializers.CharField(read_only=True)
    teacher_last_name = serializers.CharField(read_only=True)
    teacher_full_name = serializers.CharField(read_only=True)

    class Meta:
        model = TimeTable
        fields = [
            "teacher",
            "teacher_first_name",
            "teacher_last_name",
            "teacher_full_name",
        ]
