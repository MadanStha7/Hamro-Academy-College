from rest_framework import serializers

from timetable.models import TimeTable


class TeacherSubjectSerializer(serializers.ModelSerializer):
    """
    serializer to display all subject that teacher teach
    """

    subject_name = serializers.CharField(read_only=True)
    grade_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)
    teacher_first_name = serializers.CharField(read_only=True)
    teacher_last_name = serializers.CharField(read_only=True)
    subject_code = serializers.CharField(read_only=True)
    shift_name = serializers.CharField(read_only=True)
    subject_type = serializers.CharField(read_only=True, source="subject.get_subject_type_display")
    credit_hour = serializers.CharField(read_only=True)
    is_optional = serializers.CharField(read_only=True)
    day_name = serializers.CharField(source="get_day_display", read_only=True)

    class Meta:
        model = TimeTable
        read_only_fields = ["academic_session", "created_by", "institution"]
        fields = [
            "id",
            "teacher_first_name",
            "teacher_last_name",
            "day_name",
            "start_time",
            "end_time",
            "academic_session",
            "subject_name",
            "teacher",
            "subject",
            "grade",
            "grade_name",
            "section_name",
            "shift_name",
            "subject_code",
            "subject_type",
            "credit_hour",
            "is_optional"

       ]