from django.db import transaction
from rest_framework import serializers

from common.utils import to_internal_value
from student.models import StudentDocument


class StudentDocumentSerializer(serializers.ModelSerializer):

    document = serializers.CharField()


    class Meta:
        model = StudentDocument
        read_only_fields = ["institution", "created_by", "student"]
        fields = ["id", "student", "document", "name"]

    @transaction.atomic
    def create(self, validated_data):
        document = validated_data.pop("document")
        document = StudentDocument.objects.create(
                document=to_internal_value(document), **validated_data)

        return document
