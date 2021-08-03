from rest_framework import serializers
from academics.models import ApplyShift
from common.utils import validate_unique_faculty_grade


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

    # def validate(self, attrs):
    #     name = validate_unique_faculty_grade(
    #         ApplyShift, attrs, self.context.get("institution"), self.instance
    #     )
    #     return attrs

    # def create(self, validated_data):
    #     faculty_data = validated_data.pop("faculty")
    #     grade_data = validated_data.pop("grade")
    #     shift_data = validated_data.pop("shift")
    #     section_data = validated_data.pop("section")
    #
    #     apply_shift = ApplyShift.objects.create(**validated_data)
    #     apply_shift.save()
    #     return apply_shift
