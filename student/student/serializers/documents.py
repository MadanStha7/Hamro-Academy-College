from django.db import transaction
from rest_framework import serializers

from common.utils import to_internal_value
from student.models import StudentDocument


class StudentDocumentSerializer(serializers.ModelSerializer):

    document = serializers.CharField()
    document_url = serializers.SerializerMethodField(
        read_only=True, required=False, allow_null=True
    )

    def get_document_url(self, obj):
        return obj.document.url if obj.document else None

    class Meta:
        model = StudentDocument
        read_only_fields = ["institution", "created_by", "student"]
        fields = ["id", "student", "document", "document_url", "name"]
