from rest_framework import serializers
from staff.models import Designation


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "name",
        ]
