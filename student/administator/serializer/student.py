import datetime

from django.db import transaction

from rest_framework import serializers, status

from common.constant import SYSTEM_DEFAULT_PASSWORD
from common.utils import to_internal_value
from student.models import StudentInfo
from user.common.serializers.user import UserSerializer


class StudentListInfoSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(read_only=True)
    student_last_name = serializers.CharField(read_only=True)
    guardian_first_name = serializers.CharField(read_only=True)
    guardian_last_name = serializers.CharField(read_only=True)
    guardian_phone_number = serializers.CharField(read_only=True)
    roll_number = serializers.CharField(read_only=True)
    blood_group = serializers.CharField(source="get_blood_group_display")

    class Meta:
        model = StudentInfo
        fields = [
            "id",
            "admission_number",
            "student_first_name",
            "student_last_name",
            "phone",
            "photo",
            "guardian_first_name",
            "guardian_last_name",
            "guardian_phone_number",
            "address",
            "blood_group",
        ]


class StudentInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category_name = serializers.CharField(read_only=True)

    class Meta:
        model = StudentInfo
        read_only_fields = [
            "photo",
            "institution",
            "created_by",
            "created_on",
            "admission_number",
        ]
        fields = [
            "id",
            "photo",
            "admission_number",
            "user",
            "permanent_address",
            "temporary_address",
            "dob",
            "gender",
            "marital_status",
            "spouse_name",
            "blood_group",
            "religion",
            "student_category",
            "category_name",
            "guardian_detail",
            "disable",
            "institution",
            "created_by",
            "created_on",
        ]

    def validate_dob(self, value):
        if value > datetime.date.today() - datetime.timedelta(5400):
            raise serializers.ValidationError("age should be greater than 15")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            user = validated_data.pop("user")
            # photo = validated_data.pop("photo")
            student_serializer = UserSerializer(data=user)
            student_serializer.is_valid(raise_exception=True)
            student_user = student_serializer.save()
            student_user.general_info = validated_data.get("general_info")
            student = StudentInfo.objects.create(
                **validated_data,
                user=user,
            )
            student.user.username = student.admission_number
            user.set_password(SYSTEM_DEFAULT_PASSWORD)
            student.user.save()
            # if photo:
            #     student.student_photo = to_internal_value(photo)
            #     student.save()
            return student

    def update(self, instance, validated_data, *args, **kwargs):
        # photo = validated_data.pop("photo")
        with transaction.atomic():
            if validated_data.get("student_user"):
                student_data = validated_data.pop("student_user")
                student_user_serializer = UserSerializer(
                    data=student_data, instance=instance.student_user
                )
                student_user_serializer.is_valid(raise_exception=True)
                student_user_serializer.save()
            # if photo:
            #     instance.photo = to_internal_value(photo)
            #     instance.save()
            return super(StudentInfoSerializer, self).update(instance, validated_data)


