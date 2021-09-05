from academics.models import ApplyShift
from rest_framework import serializers


class ApplyShiftSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(read_only=True)
    shift_name = serializers.CharField(read_only=True)
    shift_start_time = serializers.CharField(read_only=True)
    shift_end_time = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)

    class Meta:
        model = ApplyShift
        read_only_fields = ["created_by", "institution"]
        fields = [
            "id",
            "faculty",
            "faculty_name",
            "grade",
            "grade_name",
            "shift",
            "shift_name",
            "shift_start_time",
            "shift_end_time",
            "section",
            "section_name",
            "created_by",
            "institution",
        ]
