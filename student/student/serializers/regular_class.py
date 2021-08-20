from rest_framework import serializers
from onlineclass.models import (
    OnlineClassInfo,
)


class StudentRegularClassSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)
    subject_name = serializers.CharField(read_only=True)

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
            "link_code",
            "is_regular",
        ]
