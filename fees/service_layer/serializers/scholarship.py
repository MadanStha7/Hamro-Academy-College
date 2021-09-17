from rest_framework import serializers

from common.utils import validate_unique_name
from fees.orm.models import Scholarship


class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = [
            "id",
            "name",
            "scholarship_in",
            "scholarship",
            "fee_config"
        ]

    def validate_name(self, name):
        name = validate_unique_name(
            Scholarship, name, self.context.get("institution"), self.instance
        )
        return name

    def validate(self, data):
        scholarship_in = data.get("scholarship_in")
        scholarship = data.get("scholarship")

        if scholarship_in == "P":
            if scholarship > 100:
                raise serializers.ValidationError(
                    "Scholarship percent cannot be higher than 100%"
                )
        else:
            if scholarship < 0:
                raise serializers.ValidationError("Scholarship cannot be less than 0")

        return data
