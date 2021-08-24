from rest_framework import serializers
from student.models import StudentCategory


class StudentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCategory
        read_only_fields = ["institution", "created_by"]
        fields = ["id", "name", "description"]
