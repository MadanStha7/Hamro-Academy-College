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
            "email"
        ]


class StudentInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category_name = serializers.CharField(read_only=True)
    photo = serializers.SerializerMethodField(read_only=True, required=False, allow_null=True)

    def get_photo(self, obj):
        return obj.photo.url if obj.photo else None

    class Meta:
        model = StudentInfo
        read_only_fields = [
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
            photo = validated_data.pop("photo")
            user = validated_data.pop("user")
            all_name = user["full_name"].strip().split()
            first_name, last_name = all_name[0], all_name[1:]
            last_name_all = " ".join(last_name)
            user = User.objects.create(
                phone=user.get("phone"),
                first_name=first_name,
                last_name=last_name_all,
                email=user.get("email"),
                institution=self.context.get("institution"),
            )
            student = StudentInfo.objects.create(user=user, **validated_data)
            student.user.username = student.admission_number
            user.set_password(SYSTEM_DEFAULT_PASSWORD)
            student.user.save()
            if photo:
                student.photo = to_internal_value(photo)
                student.save()

            return student

    def update(self, instance, validated_data, *args, **kwargs):
        with transaction.atomic():
            user_data = validated_data.pop("user")
            users_obj = self.instance.user
            instance.photo = validated_data.get("photo", instance.photo)
            instance.permanent_address = validated_data.get("permanent_address", instance.permanent_address)
            instance.temporary_address = validated_data.get("temporary_address", instance.temporary_address)
            instance.dob = validated_data.get("dob", instance.dob)
            userserializer = UserSerializer(users_obj, data=user_data, partial=True)
            if userserializer.is_valid(raise_exception=True):
                full_name = userserializer.validated_data["full_name"].strip().split()
                first_name, last_name = full_name[0], full_name[1:]
                userserializer.save()
                last_name_all = " ".join(last_name)
                user_data_obj = User.objects.get(id=self.instance.user.id)
                user_data_obj.first_name = first_name
                user_data_obj.last_name = last_name_all
                user_data_obj.save()
            return instance



