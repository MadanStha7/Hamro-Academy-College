from rest_framework import serializers

from common.utils import validate_unique_name
from fees.models import FineType


class FineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FineType
        fields = [
            "id",
            "name",
            "fine_mode",
            "fine_amount",
        ]

    def validate_name(self, name):
        name = validate_unique_name(
            FineType, name, self.context.get("institution"), self.instance
        )
        return name
