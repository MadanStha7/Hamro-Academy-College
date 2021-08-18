from rest_framework import serializers
from django.utils import timezone
import datetime
from onlineclass.administrator.serializers.online_class import OnlineClassSerializer
from onlineclass.models import (
    StudentOnlineClassAttendance,
    OnlineClassInfo,
)


class StudentOnlineClassAttendanceSerializer(serializers.ModelSerializer):
    onlineclass_title = serializers.CharField(read_only=True)
    student_full_name = serializers.CharField(read_only=True)

    class Meta:
        model = StudentOnlineClassAttendance
        read_only_fields = ["created_by", "institution"]
        fields = (
            "id",
            "online_class",
            "onlineclass_title",
            "student_academic",
            "student_full_name",
            "joined_on",
        )

    def validate_online_class(self, value):
        time_now = timezone.now().strftime("%H:%M")
        if OnlineClassInfo.objects.filter(
            id=value.id, class_date__lt=datetime.date.today(), end_time__lt=time_now
        ).exists():
            raise serializers.ValidationError("class link already expired")
        return value
