from rest_framework import serializers
from onlineclass.models import StudentOnlineClassAttendance


class StudentOnlineClassAttendanceSerializer(serializers.ModelSerializer):
    onlineclass_title = serializers.CharField(read_only=True)
    onlineclass_start_time = serializers.CharField(
        read_only=True, source="online_class.start_time"
    )
    onlineclass_end_time = serializers.CharField(
        read_only=True, source="online_class.end_time"
    )
    subject_name = serializers.CharField(read_only=True)

    class Meta:
        model = StudentOnlineClassAttendance
        read_only_fields = ["created_by", "institution"]
        fields = (
            "id",
            "onlineclass_title",
            "onlineclass_start_time",
            "onlineclass_end_time",
            "subject_name",
            "joined_on",
            "created_on",
        )
