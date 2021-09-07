import datetime
from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from common.constant import SYSTEM_DEFAULT_PASSWORD
from common.utils import validate_unique_phone, to_internal_value

from student.models import StudentInfo

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "phone", "first_name", "middle_name", "last_name", "email")

        extra_kwargs = {
            "phone": {"validators": []},
        }


class StudentListInfoSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(read_only=True)
    student_middle_name = serializers.CharField(read_only=True)
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
            "student_middle_name",
            "student_last_name",
            "faculty",
            "grade",
            "section",
            "guardian_first_name",
            "guardian_last_name",
            "relation",
            "phone",
            "email",
            "status",
        ]


class StudentInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category_name = serializers.CharField(read_only=True)
    student_first_name = serializers.CharField(read_only=True)
    student_middle_name = serializers.CharField(read_only=True)
    student_last_name = serializers.CharField(read_only=True)
    blood_group_display = serializers.CharField(
        read_only=True, source="get_blood_group_display"
    )
    religion_display = serializers.CharField(
        read_only=True, source="get_religion_display"
    )
    gender_display = serializers.CharField(read_only=True, source="get_gender_display")
    photo = serializers.SerializerMethodField(
        read_only=True, required=False, allow_null=True
    )

    def get_photo(self, obj):
        return obj.photo.url if obj.photo else None

    class Meta:
        model = StudentInfo
        read_only_fields = [
            "institution",
            "status",
            "created_by",
            "created_on",
            "admission_number",
        ]
        fields = [
            "id",
            "photo",
            "admission_number",
            "user",
            "student_first_name",
            "student_middle_name",
            "student_last_name",
            "permanent_address",
            "temporary_address",
            "dob",
            "gender",
            "gender_display",
            "blood_group",
            "blood_group_display",
            "religion",
            "religion_display",
            "student_category",
            "category_name",
            "guardian_detail",
            "disable",
            "status",
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
            raise serializers.ValidationError(
                "length of phone number should be more than 7 and less than 14!"
            )
        return user

    def create(self, validated_data):

        with transaction.atomic():
            photo = validated_data.pop("photo")
            user = validated_data.pop("user")
            user = User.objects.update_or_create(
                phone=user.get("phone"),
                defaults={
                    "first_name": user.get("first_name"),
                    "last_name": user.get("last_name"),
                    "middle_name": user.get("middle_name"),
                    "email": user.get("email"),
                    "institution": self.context.get("institution"),
                },
            )
            print("user", user)
            student = StudentInfo(user=user, **validated_data)

            created_by = validated_data.get("created_by")
            for item in created_by.roles.all():
                if item.title == "Administrator":
                    student.status = "A"

                elif item.title == "Front Desk Officer":
                    student.status = "D"
                else:
                    pass
            student.save()
            student.user.username = student.admission_number
            user.set_password(SYSTEM_DEFAULT_PASSWORD)
            student.user.save()
            if photo:
                student.photo = to_internal_value(photo)
                student.save()

            return student

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        users_obj = self.instance.user
        userSerializer = UserSerializer(users_obj, data=user_data, partial=True)
        if userSerializer.is_valid(raise_exception=True):
            if validated_data.get("photo"):
                instance.photo = to_internal_value(validated_data.pop("photo"))
                instance.save()
            if validated_data.get("user"):
                student_data = validated_data.pop("user")
                user_serializer = UserSerializer(
                    data=student_data, instance=instance.user
                )
                user_serializer.is_valid(raise_exception=True)
                print(user_serializer.validated_data.get("phone"))
                user, created = User.objects.update_or_create(
                    phone=user_serializer.validated_data.get("phone"),
                    defaults={**user_serializer.validated_data},
                )
                instance.user = user
            return super(StudentInfoSerializer, self).update(instance, validated_data)
