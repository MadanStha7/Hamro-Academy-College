from rest_framework import serializers
from onlineclass.models import StudentOnlineClassAttendance


class StudentOnlineClassAttendanceSerializer(serializers.ModelSerializer):
    onlineclass_title = serializers.CharField(read_only=True)
    student_name = serializers.CharField(read_only=True)

    class Meta:
        model = StudentOnlineClassAttendance
        read_only_fields = ["created_by", "institution"]
        fields = (
            "id",
            "online_class",
            "onlineclass_title",
            "student_academic",
            "student_name",
            "joined_on",
        )
