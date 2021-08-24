from rest_framework import serializers
from general.models import AcademicSession
from common.utils import validate_unique_name
from common.utils import return_grade_name_of_value
from academics.models import Grade


class AcademicSessionSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(read_only=True)

    class Meta:
        model = AcademicSession
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "name",
            "from_date",
            "to_date",
            "status",
            "created_by",
            "institution",
            # "grade",
            "grade_name",
        ]
