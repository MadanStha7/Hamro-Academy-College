from rest_framework import serializers
from staff.models import Document
from django.db import transaction


class DocumentSerializer(serializers.ModelSerializer):
    document = serializers.ListField(
        child=serializers.FileField(max_length=100000), write_only=True
    )
    document_name = serializers.SerializerMethodField(read_only=True)

    def get_document_name(self, obj):
        return Document.objects.filter(staff=obj.staff).values("document")

    class Meta:
        model = Document
        read_only_fields = ["institution", "created_by"]
        fields = ["id", "staff", "document", "name", "document_name"]

    @transaction.atomic
    def create(self, validated_data):
        document = validated_data.pop("document")
        for doc in document:
            document = Document.objects.create(document=doc, **validated_data)
        return document
