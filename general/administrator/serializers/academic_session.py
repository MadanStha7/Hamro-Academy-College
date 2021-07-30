from rest_framework import serializers
from general.models import AcademicSession
from common.utils import validate_unique_name


class AcademicSessionSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(source="grade.name", read_only=True)

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
            "grade_name",
        ]

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
