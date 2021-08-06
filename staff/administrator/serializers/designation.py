from rest_framework import serializers
from staff.models import Designation
from common.utils import validate_unique_name


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "name",
        ]

    def validate_name(self, name):
        """check that designation is already exist"""
        name = validate_unique_name(
            Designation, name, self.context.get("institution"), self.instance
        )
        return name
