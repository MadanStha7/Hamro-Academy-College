from rest_framework import serializers
from academics.models import Faculty
from common.utils import validate_unique_name


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        read_only_fields = ["institution", "created_by"]
        fields = ["id", "name", "created_by", "institution"]

    def validate_name(self, name):
        """check that faculty name is already exist"""
        name = validate_unique_name(
            Faculty, name, self.context.get("institution"), self.instance
        )
        return name
