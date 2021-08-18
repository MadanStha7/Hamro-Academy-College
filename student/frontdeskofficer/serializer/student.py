import datetime
from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from common.constant import SYSTEM_DEFAULT_PASSWORD
from common.utils import validate_unique_phone, to_internal_value
from staff.administrator.serializers.staff import UserSerializer
from student.models import StudentInfo


User = get_user_model()


class StudentListInfoSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(read_only=True)
    student_last_name = serializers.CharField(read_only=True)
    guardian_first_name = serializers.CharField(read_only=True)
    guardian_last_name = serializers.CharField(read_only=True)
    faculty = serializers.CharField(read_only=True)
    grade = serializers.CharField(read_only=True)
    section = serializers.CharField(read_only=True)
    relation = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    class Meta:
        model = StudentInfo
        fields = [
            "id",
            "student_first_name",
            "student_last_name",
            "faculty",
            "grade",
            "section",
            "guardian_first_name",
            "guardian_last_name",
            "relation",
            "phone",
            "email",
        ]
