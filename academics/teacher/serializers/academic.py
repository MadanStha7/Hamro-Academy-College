from rest_framework import serializers
from timetable.models import TimeTable


class GradeSerializer(serializers.ModelSerializer):
    """
    serializer to get teacher grade where teacher has been assigned
    """

    grade_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)

    class Meta:
        model = TimeTable
        fields = ["id", "grade", "grade_name", "section", "section_name"]


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
    faculty_name = serializers.CharField(read_only=True)
    day_name = serializers.CharField(source="get_day_display", read_only=True)

    class Meta:
        model = TimeTable
        fields = [
            "id",
            "shift",
            "shift_name",
            "section_name",
            "grade_name",
            "start_time",
            "end_time",
            "subject_name",
            "day_name",
            "faculty_name"
        ]


class SectionSerializer(serializers.ModelSerializer):
    """
    serializer to get teacher section where teacher has been assigned
    """

    section_name = serializers.CharField(read_only=True)

    class Meta:
        model = TimeTable
        fields = ["id", "section", "section_name"]


class ClassSerializer(serializers.ModelSerializer):
    """
    serializer to get teacher grade where teacher has been assigned
    """

    grade_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)

    class Meta:
        model = TimeTable
        fields = ["id", "grade", "grade_name", "section", "section_name", "faculty", "faculty_name"]
