from rest_framework import serializers
from academics.models import ApplyShift


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

    def create(self, validated_data):
        faculty_data = validated_data.pop("faculty")
        grade_data = validated_data.pop("grade")
        shift_data = validated_data.pop("shift")
        section_data = validated_data.pop("section")

        apply_shift = ApplyShift.objects.get(
            faculty__name=faculty_data, grade=grade_data, shift=shift_data
        )
        print("...........", apply_shift.id)
        if apply_shift:
            section = apply_shift.section.set(section_data)
            print(section)
        return apply_shift
