from rest_framework import serializers

from academics.administrator.serializers.section import SectionSerializer
from academics.models import Class, Faculty
from timetable.models import TimeTable


class GradeSerializer(serializers.ModelSerializer):
    """
    serializer to get teacher grade where teacher has been assigned
    """

    grade_name = serializers.CharField(read_only=True)
    section = SectionSerializer(read_only=True)

    class Meta:
        model = TimeTable
        fields = ["id", "grade", "grade_name", "section"]


class FacultySerializer(serializers.ModelSerializer):
    """
    serializer to get the teacher teaching faculty
    """
    faculty_name = serializers.CharField(read_only=True)

    class Meta:
        model = TimeTable
        fields = ["id", "faculty", "faculty_name"]


class ShiftSerializer(serializers.ModelSerializer):
    """
    serializer to get the teacher teaching shift
    """
    shift_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)
    grade_name = serializers.CharField(read_only=True)
    subject_name = serializers.CharField(read_only=True)
    shift_time = serializers.CharField(read_only=True)

    class Meta:
        model = TimeTable
        fields = [
            "id",
            "shift",
            "shift_name",
            "section_name",
            "grade_name",
            "shift_time",
            "subject_name"
        ]

