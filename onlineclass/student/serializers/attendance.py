from rest_framework import serializers
from onlineclass.models import StudentOnlineClassAttendance


class StudentOnlineClassAttendanceSerializer(serializers.ModelSerializer):
    onlineclass_title = serializers.CharField(read_only=True)
    subject_name = serializers.CharField(read_only=True)

    class Meta:
        model = StudentOnlineClassAttendance
        read_only_fields = ["created_by", "institution"]
        fields = (
            "id",
            "online_class",
            "onlineclass_title",
            "subject_name",
            "student_academic",
            "joined_on",
        )
