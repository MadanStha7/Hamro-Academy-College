from rest_framework import serializers
from common.utils import validate_unique_name
from fees.models import DiscountType


class DiscountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountType
        fields = [
            "id",
            "name",
            "discount_mode",
            "discount_amount",
        ]

    def validate_name(self, name):
        name = validate_unique_name(
            DiscountType, name, self.context.get("institution"), self.instance
        )
        return name

