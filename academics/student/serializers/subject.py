from rest_framework import serializers
from timetable.models import TimeTable
from common.utils import get_subject_type_name_of_value


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

    def to_representation(self, data):
        data = super(StudentSubjectSerializer, self).to_representation(data)
        data["subject_type"] = get_subject_type_name_of_value(data["subject_type"])
        return data
