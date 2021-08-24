from rest_framework import serializers
from academics.models import Faculty


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        read_only_fields = ["institution", "created_by"]
        fields = ["id", "name", "created_by", "institution"]
