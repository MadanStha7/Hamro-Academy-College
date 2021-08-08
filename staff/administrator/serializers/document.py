from rest_framework import serializers
from staff.models import Document
from django.db import transaction
from common.utils import to_internal_value


class DocumentSerializer(serializers.ModelSerializer):

    document = serializers.CharField()
    document_name = serializers.SerializerMethodField(
        read_only=True, required=False, allow_null=True
    )

    def get_document_name(self, obj):
        return obj.document.url if obj.document else None

    class Meta:
        model = Document
        read_only_fields = ["institution", "created_by", "staff"]
        fields = ["id", "staff", "document", "name", "document_name"]

    @transaction.atomic
    def create(self, validated_data):
        print(validated_data)
        document = validated_data.pop("document")
        document = Document.objects.create(
            document=to_internal_value(document), **validated_data
        )
        return document
