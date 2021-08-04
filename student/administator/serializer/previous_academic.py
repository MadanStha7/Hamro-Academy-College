from rest_framework import serializers
from student.models import PreviousAcademicDetail


class PreviousAcademicSerializer(serializers.ModelSerializer):
    """
    serializer to list the student academic of student
    """

    class Meta:
        model = PreviousAcademicDetail

        read_only_fields = ["created_by", "institution"]
        fields = [
            "id",
            "student",
            "last_school",
            "address",
            "phone",
            "email",
            "created_by",
            "institution",
        ]
