from academics.models import Faculty, Grade
from rest_framework import serializers
import datetime
from common.utils import validate_unique_name
from fees.models import FeeSetup
from academics.administrator.serializers.faculty import FacultySerializer
from academics.administrator.serializers.grade import GradeSerializer


class FeeSetupSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True, many=True)
    grade = GradeSerializer(read_only=True, many=True)
    faculty_id = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), source="faculty", write_only=True, many=True
    )
    grade_id = serializers.PrimaryKeyRelatedField(
        queryset=Grade.objects.all(), source="grade", write_only=True, many=True
    )

    class Meta:
        model = FeeSetup
        fields = [
            "id",
            "name",
            "faculty",
            "faculty_id",
            "grade",
            "grade_id",
            "due_date",
        ]

    def validate_name(self, name):
        name = validate_unique_name(
            FeeSetup, name, self.context.get("institution"), self.instance
        )
        return name

    def validate_due_date(self, value):
        if not self.instance:
            if value and value < datetime.date.today():
                raise serializers.ValidationError("Due date cannot be past date.")
        return value
