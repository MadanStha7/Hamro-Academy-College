from rest_framework import serializers
from academics.models import (
    Section,
)


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        read_only_fields = ["created_by", "institution"]
        fields = ["id", "name", "created_by", "institution"]
