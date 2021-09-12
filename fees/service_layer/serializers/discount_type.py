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

    def validate(self, data):
        discount_mode = data.get("discount_mode")
        discount_amount = data.get("discount_amount")

        if discount_mode == "P":
            if discount_amount > 100:
                raise serializers.ValidationError(
                    "Discount percent cannot be higher than 100%"
                )
        else:
            if discount_amount < 0:
                raise serializers.ValidationError(
                    "Discount amount cannot be less than 0"
                )

        return data
