from rest_framework import serializers
from academics.models import Shift


class ShiftSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(read_only=True)

    class Meta:
        model = Shift
        read_only_fields = ["created_by", "institution"]
        fields = [
            "id",
            "name",
            "start_time",
            "end_time",
            "faculty_name",
            "created_by",
            "institution",
        ]
