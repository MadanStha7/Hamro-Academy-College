from rest_framework import serializers

from academics.helpers import validate_start_end_time, validate_date
from onlineclass.models import OnlineClassInfo


class OnlineClassInfoSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(read_only=True)
    teacher_first_name = serializers.CharField(read_only=True)
    teacher_last_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)
    grade_name = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)
    class_date = serializers.DateField(required=True)

    class Meta:
        model = OnlineClassInfo
        fields = [
            "id",
            "subject",
            "teacher_first_name",
            "teacher_last_name",
            "subject_name",
            "class_date",
            "start_time",
            "end_time",
            "grade",
            "grade_name",
            "section",
            "section_name",
            "faculty",
            "faculty_name",
            "link_code",
        ]

    def validate(self, value):
        validate_start_end_time(value)
        return super(OnlineClassInfoSerializer, self).validate(value)

    def validate_class_date(self, value):
        value = validate_date(value)
        return value


class TeacherStudentOnlineClassAttendanceSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)
    subject_name = serializers.CharField(read_only=True)
    student_first_name = serializers.CharField(read_only=True)
    student_last_name = serializers.CharField(read_only=True)
    online_class = OnlineClassInfoSerializer(read_only=True)

    class Meta:
        # model = StudentOnlineClassAttendance
        read_only_fields = ["link"]
        fields = (
            "id",
            "online_class",
            "student_academic",
            "joined_on",
            "created_on",
            "modified_on",
            "grade_name",
            "section_name",
            "subject_name",
            "student_first_name",
            "student_last_name",
        )