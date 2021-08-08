from academics.models import ApplyShift
from common.utils import validate_unique_faculty_grade
from rest_framework import serializers
from django.db import transaction


class ApplyShiftSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(read_only=True)
    shift_name = serializers.CharField(read_only=True)
    shift_start_time = serializers.CharField(read_only=True)
    shift_end_time = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)

    class Meta:
        model = ApplyShift
        read_only_fields = ["created_by", "institution"]
        fields = [
            "id",
            "faculty",
            "faculty_name",
            "grade",
            "grade_name",
            "shift",
            "shift_name",
            "shift_start_time",
            "shift_end_time",
            "section",
            "created_by",
            "institution",
        ]

    @transaction.atomic
    def create(self, validated_data):
        faculty_data = validated_data.pop("faculty")
        grade_data = validated_data.pop("grade")
        shift_data = validated_data.pop("shift")
        section_data = validated_data.pop("section")
        instance, created = ApplyShift.objects.update_or_create(
            faculty=faculty_data,
            grade=grade_data,
            shift=shift_data,
            defaults={**validated_data},
        )
        if section_data is not None:
            instance.section.set(section_data)
            instance.save()
        return instance
