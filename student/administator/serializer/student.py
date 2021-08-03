import datetime

from django.db import transaction
from rest_framework import serializers

from common.constant import SYSTEM_DEFAULT_PASSWORD
from student.models import StudentInfo
from user.administrator.serializers.user import UserSerializer


class StudentListInfoSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(read_only=True)
    student_last_name = serializers.CharField(read_only=True)
    guardian_first_name = serializers.CharField(read_only=True)
    guardian_last_name = serializers.CharField(read_only=True)
    guardian_phone_number = serializers.CharField(read_only=True)
    section = serializers.CharField(read_only=True)
    roll_number = serializers.CharField(read_only=True)
    grade = serializers.CharField(read_only=True)
    blood_group = serializers.CharField(source="get_blood_group_display")

    class Meta:
        model = StudentInfo
        fields = [
            "id",
            "admission_number",
            "student_first_name",
            "student_last_name",
            "phone_number",
            "student_photo",
            "guardian_first_name",
            "guardian_last_name",
            "guardian_phone_number",
            "grade",
            "section",
            "roll_number",
            "address",
            "blood_group",
        ]


class StudentInfoSerializer(serializers.ModelSerializer):
    student_user = UserSerializer()
    category_name = serializers.CharField(
        source="student_category.name", read_only=True
    )
    blood_group_display = serializers.CharField(
        source="get_blood_group_display", read_only=True
    )

    class Meta:
        model = StudentInfo
        read_only_fields = ["institution", "admission_number"]
        fields = [
            "id",
            "photo",
            "admission_number",
            "user",
            "address",
            "dob",
            "gender",
            "blood_group",
            "blood_group_display",
            "phone",
            "student_category",
            "category_name",
            "religion",
            "medical_history",
            "transportation_detail",
            "guardian_detail",
            "disable",
            "institution",
            "created_by",
            "created_on",
        ]

    def validate_date_of_birth(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError(
                "Student date of birth must be a valid date"
            )
        return value

    def validate_guardian_detail(self, guardian_detail):
        if StudentInfo.objects.filter(guardian_detail__id=guardian_detail).exists():
            raise serializers.ValidationError(
                "Student with same guardian detail already exists"
            )

    def create(self, validated_data):
        with transaction.atomic():
            student_user = validated_data.pop("student_user")
            student_serializer = UserSerializer(data=student_user)
            student_serializer.is_valid(raise_exception=True)
            student_user = student_serializer.save()
            student_user.general_info = validated_data.get("general_info")
            student = StudentInfo.objects.create(
                **validated_data,
                student_user=student_user,
            )
            student.student_user.username = student.admission_number
            student_user.set_password(SYSTEM_DEFAULT_PASSWORD)
            student.student_user.save()
            return student

    def update(self, instance, validated_data, *args, **kwargs):
        with transaction.atomic():
            if validated_data.get("student_user"):
                student_data = validated_data.pop("student_user")
                student_user_serializer = UserSerializer(
                    data=student_data, instance=instance.student_user
                )
                student_user_serializer.is_valid(raise_exception=True)
                student_user_serializer.save()
            return super(StudentInfoSerializer, self).update(instance, validated_data)
