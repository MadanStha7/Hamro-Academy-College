from rest_framework import serializers
from general.models import AcademicSession
from common.utils import validate_unique_name
from common.utils import return_grade_name_of_value
from academics.models import Faculty, Grade


class AcademicSessionSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(read_only=True)

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
            "grade",
            "faculty",
            "faculty_name"
            # "grade_name",
        ]

    def to_representation(self, data):
        data = super(AcademicSessionSerializer, self).to_representation(data)
        data["grade_name"] = return_grade_name_of_value(
            Grade.objects.get(id=data["grade"]).name
        )
        return data

    def validate_name(self, name):
        """check that academic session is already exist"""
        name = validate_unique_name(
            AcademicSession, name, self.context.get("institution"), self.instance
        )
        return name

    def validate(self, attrs):
        """
        Check that to date should be greater than from date
        """
        from_date = attrs.get("from_date")
        to_date = attrs.get("to_date")
        if to_date <= from_date:
            raise serializers.ValidationError(
                "from_date should not be greater than or equal to_date"
            )

        return attrs
