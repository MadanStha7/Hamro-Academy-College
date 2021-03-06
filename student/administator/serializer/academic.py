from django.db import transaction
from rest_framework import serializers
from student.administator.serializer.previous_academic import PreviousAcademicSerializer
from student.models import StudentAcademicDetail, PreviousAcademicDetail


class StudentAcademicSerializer(serializers.ModelSerializer):
    """
    serializer to list the previous student academic of student
    """
    section_name = serializers.CharField(read_only=True)
    grade_name = serializers.CharField(read_only=True)
    faculty_name = serializers.CharField(read_only=True)
    shift_name = serializers.CharField(read_only=True)

    class Meta:
        model = StudentAcademicDetail

        read_only_fields = ["created_by", "institution", "academic_session", "student"]
        fields = [
            "id",
            "student",
            "grade",
            "grade_name",
            "section",
            "section_name",
            "faculty_name",
            "faculty",
            "shift",
            "shift_name",
            "academic_session",
            "institution"
        ]


class StudentAcademicDetailSerializer(serializers.Serializer):
    previous_academic = PreviousAcademicSerializer()
    student_academic = StudentAcademicSerializer()
    created_by = serializers.CharField(read_only=True)
    institution = serializers.CharField(read_only=True)

    def create(self, validated_data):
        with transaction.atomic():
            previous_details = validated_data.pop("previous_academic")
            student_academics = validated_data.pop("student_academic")
            previous_academic, created = PreviousAcademicDetail.objects.update_or_create(
                    student=previous_details.get("student"), defaults={**previous_details}
                )
            student_academic, created = StudentAcademicDetail.objects.update_or_create(
                student=student_academics.get("student"), academic_session__status=True,
                defaults={**student_academics}
            )
            context = {"student_academic": student_academic,
                       "previous_academic": previous_academic}
            return context
