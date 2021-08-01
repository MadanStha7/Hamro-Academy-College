from rest_framework import serializers
from staff.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        read_only_fields = ["institution", "created_by"]
        fields = ["id", "staff", "document", "name"]
