from student.models import StudentAcademicDetail
from rest_framework import serializers
from django.utils import timezone
import datetime
from onlineclass.administrator.serializers.online_class import OnlineClassSerializer
from onlineclass.models import (
    StudentOnlineClassAttendance,
    OnlineClassInfo,
)


class StudentOnlineClassAttendanceSerializer(serializers.ModelSerializer):
    onlineclass_title = serializers.CharField(
        read_only=True, source="online_class.title"
    )
    onlineclass_start_time = serializers.CharField(
        read_only=True, source="online_class.start_time"
    )
    onlineclass_end_time = serializers.CharField(
        read_only=True, source="online_class.end_time"
    )
    onlineclass_subject = serializers.CharField(
        read_only=True, source="online_class.subject.name"
    )
    student_full_name = serializers.CharField(read_only=True)

    class Meta:
        model = StudentOnlineClassAttendance
        read_only_fields = ["created_by", "institution"]
        fields = (
            "onlineclass_title",
            "onlineclass_start_time",
            "onlineclass_end_time",
            "onlineclass_subject",
            "student_full_name",
            "joined_on",
            "created_on",
        )

    def validate_online_class(self, value):
        time_now = timezone.now().strftime("%H:%M")
        if OnlineClassInfo.objects.filter(
            id=value.id, class_date__lt=datetime.date.today(), end_time__lt=time_now
        ).exists():
            raise serializers.ValidationError("class link already expired")
        return value


class StudentAcademicSerializer(serializers.ModelSerializer):

    section_name = serializers.CharField(read_only=True, source="section.name")
    grade_name = serializers.CharField(read_only=True, source="grade.name")
    faculty_name = serializers.CharField(read_only=True, source="faculty.name")
    subject_name = serializers.CharField(
        read_only=True, source="student_online_class_attendance.subject.name"
    )
    student_full_name = serializers.CharField(
        source="student.user.get_full_name", read_only=True
    )
    online_class_attendance = serializers.SerializerMethodField()

    def get_online_class_attendance(self, obj):
        student_online_class_attendence_obj = (
            StudentOnlineClassAttendance.objects.filter(
                online_class=self.context.get("online_class"),
                student_academic=obj.id,
                institution=self.context.get("institution"),
            )
        )
        if student_online_class_attendence_obj is not None:
            serializer = StudentOnlineClassAttendanceSerializer(
                student_online_class_attendence_obj, many=True
            )
            return serializer.data

    class Meta:

        model = StudentAcademicDetail
        read_only_fields = ["created_by", "institution", "academic_session", "student"]
        fields = [
            "student_full_name",
            "section_name",
            "grade_name",
            "faculty_name",
            "subject_name",
            "online_class_attendance",
        ]
