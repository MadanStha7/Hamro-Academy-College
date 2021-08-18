from rest_framework import serializers

from academics.helpers import validate_start_end_time, validate_date
from onlineclass.models import OnlineClassInfo, StudentOnlineClassAttendance


class OnlineClassInfoSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)
    subject_name = serializers.CharField(read_only=True)
    teacher_first_name = serializers.CharField(read_only=True)
    teacher_last_name = serializers.CharField(read_only=True)
    class_date = serializers.DateField(required=True)

    class Meta:
        model = OnlineClassInfo
        fields = [
            "id",
            "title",
            "subject",
            "subject_name",
            "class_date",
            "days",
            "start_time",
            "end_time",
            "grade",
            "grade_name",
            "section",
            "section_name",
            "faculty",
            "faculty_name",
            "teacher_first_name",
            "teacher_last_name",
            "link_code",
            "is_regular"
        ]

    def validate(self, value):
        validate_start_end_time(value)
        return super(OnlineClassInfoSerializer, self).validate(value)

    def validate_class_date(self, value):
        value = validate_date(value)
        return value


class TeacherStudentOnlineClassAttendanceSerializer(serializers.ModelSerializer):
    online_class_title = serializers.CharField(read_only=True)
    student_first_name = serializers.CharField(read_only=True)
    student_last_name = serializers.CharField(read_only=True)
    grade_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)
    subject_name = serializers.CharField(read_only=True)
    online_class = OnlineClassInfoSerializer(read_only=True)

    class Meta:
        model = StudentOnlineClassAttendance
        read_only_fields = ["created_by", "institution"]
        fields = (
            "id",
            "online_class",
            "online_class_title",
            "student_academic",
            "student_first_name",
            "student_last_name",
            "grade_name",
            "section_name",
            "faculty_name",
            "subject_name",
            "joined_on",
        )