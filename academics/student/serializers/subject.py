from rest_framework import serializers
from timetable.models import TimeTable


class StudentSubjectSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(read_only=True)
    subject_credit_hour = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )
    subject_type = serializers.CharField(read_only=True)

    class Meta:
        model = TimeTable
        fields = [
            "subject",
            "subject_name",
            "subject_credit_hour",
            "subject_type",
        ]
