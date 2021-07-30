from rest_framework import serializers
from academics.models import (
    Section,
)
from common.utils import validate_unique_name


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        read_only_fields = ["created_by", "institution"]
        fields = ["id", "name", "created_by", "institution"]

    def validate_name(self, name):
        name = validate_unique_name(
            Section, name, self.context.get("institution"), self.instance
        )
        return name
