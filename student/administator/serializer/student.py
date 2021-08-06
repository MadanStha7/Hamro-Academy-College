import datetime
from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from common.constant import SYSTEM_DEFAULT_PASSWORD
from common.utils import validate_unique_phone
from student.models import StudentInfo
from user.common.serializers.user import UserSerializer


User = get_user_model()


class StudentListInfoSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(read_only=True)
    student_last_name = serializers.CharField(read_only=True)
    guardian_first_name = serializers.CharField(read_only=True)
    guardian_last_name = serializers.CharField(read_only=True)
    guardian_phone_number = serializers.CharField(read_only=True)
    roll_number = serializers.CharField(read_only=True)
    blood_group = serializers.CharField(source="get_blood_group_display")
    phone = serializers.CharField(read_only=True)

    class Meta:
        model = StudentInfo
        fields = [
            "id",
            "roll_number",
            "admission_number",
            "student_first_name",
            "student_last_name",
            "phone",
            "photo",

            "guardian_first_name",
            "guardian_last_name",
            "guardian_phone_number",
            "temporary_address",
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

    def validate_user(self, user):
        """check that faculty name is already exist"""
        phone = user.get("phone")
        # phone number between 7 to 14
        if len(phone) < 7 or len(phone) > 14:
            raise serializers.ValidationError("length of phone number should be more than 7 and less than 14!")
        phone = validate_unique_phone(
            User, phone, self.context.get("institution"), self.instance
        )
        return user

    def create(self, validated_data):
        with transaction.atomic():

            user = validated_data.pop("user")
            user = User.objects.create(
                first_name=user.get("first_name"),
                last_name=user.get("last_name"),
                email=user.get("email"),
                phone=user.get("phone"),
                institution=self.context.get("institution"),
            )
            student = StudentInfo.objects.create(user=user, **validated_data)
            student.user.username = student.admission_number
            user.set_password(SYSTEM_DEFAULT_PASSWORD)
            student.user.save()
            return student

    def update(self, instance, validated_data, *args, **kwargs):
        with transaction.atomic():
            if validated_data.get("user"):
                student_data = validated_data.pop("user")
                student_user_serializer = UserSerializer(
                    data=student_data, instance=instance.user
                )
                student_user_serializer.is_valid(raise_exception=True)
                student_user_serializer.save()
            return super(StudentInfoSerializer, self).update(instance, validated_data)


