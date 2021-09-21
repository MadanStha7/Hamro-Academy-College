from rest_framework import serializers

from common.utils import validate_unique_name
from fees.orm.models import FineType


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

    def validate(self, data):
        fine_mode = data.get("fine_mode")
        fine_amount = data.get("fine_amount")

        if fine_mode == "P":
            if fine_amount > 100:
                raise serializers.ValidationError(
                    "Fine percent cannot be higher than 100%"
                )
        else:
            if fine_amount < 0:
                raise serializers.ValidationError("Fine amount cannot be less than 0")

        return data
