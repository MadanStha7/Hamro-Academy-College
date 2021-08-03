from rest_framework import serializers
from .models import InstitutionInfo


class InstitutionInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = InstitutionInfo
        fields = (
            "id",
            "logo",
            "name",
            "abbreviation",
            "address",
            "phone_number",
            "email",
            "slogan",
            "reg_number",
        )
