from rest_framework import serializers
from staff.models import Staff
from user.administrator.serializers.role import RoleSerializer
from common.utils import (
    validate_unique_phone,
    validate_unique_email,
    return_marital_status_value,
    return_designation_name,
)
from academics.models import Faculty, Grade
from common.utils import to_internal_value
from django.db import transaction
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "phone", "email", "first_name", "middle_name", "last_name")

        extra_kwargs = {
            "phone": {"validators": []},
        }


class StaffSerializer(serializers.ModelSerializer):
    photo = serializers.CharField()
    designation__name = serializers.CharField(read_only=True)
    user = UserSerializer()

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res["roles"] = RoleSerializer(
            instance.user.roles.all().values("id", "title"), many=True
        ).data
        res["marital_status_value"] = return_marital_status_value(res["marital_status"])
        return res

    class Meta:
        model = Staff
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "photo",
            "user",
            "designation",
            "address",
            "dob",
            "marital_status",
            "spouse_name",
            "designation__name",
            "marital_status",
        ]

    def validate(self, attrs):
        compare_date = date.today().year - attrs["dob"].year
        if compare_date < 15:
            raise serializers.ValidationError("age should be greater than 15")
        return attrs

    def validate_user(self, user):
        phone = user.get("phone")
        email = user.get("email")

        # phone number between 10 to 15
        if len(phone) < 10 or len(phone) > 15:
            raise serializers.ValidationError("enter the correct phone number!")

        if email:
            email = validate_unique_email(
                User, email, self.context.get("institution"), self.instance
            )
        return user

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data.pop("user")
        photo = validated_data.pop("photo")

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
        staff = Staff.objects.create(user=user, **validated_data)
        staff.save()

        # user = User.objects.create(
        #     first_name=user.get("first_name"),
        #     middle_name=user.get("middle_name"),
        #     last_name=user.get("last_name"),
        #     phone=user.get("phone"),
        #     email=user.get("email"),
        #     institution=self.context.get("institution"),
        # )
        return staff

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        users_obj = self.instance.user
        userSerializer = UserSerializer(users_obj, data=user_data, partial=True)
        if userSerializer.is_valid(raise_exception=True):
            user_data_obj = User.objects.get(id=self.instance.user.id)
            user_data_obj.first_name = user_data.get("first_name")
            user_data_obj.middle_name = user_data.get("middle_name")
            user_data_obj.last_name = user_data.get("last_name")
            user_data_obj.email = user_data.get("email")
            user_data_obj.phone = user_data.get("phone")
            user_data_obj.save()
        super(StaffSerializer, self).update(instance, validated_data)
        return instance


class StaffListSerializer(serializers.ModelSerializer):
    designation__name = serializers.CharField(read_only=True)
    gender_name = serializers.CharField(source="get_gender_display", read_only=True)
    religion_name = serializers.CharField(source="get_religion_display", read_only=True)
    blood_group_name = serializers.CharField(
        source="get_blood_group_display", read_only=True
    )

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res["user"] = UserSerializer(instance.user).data
        res["marital_status_value"] = return_marital_status_value(res["marital_status"])
        res["designation"] = return_designation_name(res["id"])
        return res

    class Meta:
        model = Staff
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "photo",
            "address",
            "blood_group_name",
            "religion_name",
            "designation__name",
            "gender_name",
            "user",
            "marital_status",
        ]


class StaffAssignSerialzer(serializers.ModelSerializer):
    phone = serializers.CharField()
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return obj.roles.all().values("title")

    class Meta:
        model = User
        fields = ("id", "phone", "roles")
