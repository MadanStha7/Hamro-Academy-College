from rest_framework import serializers
from staff.models import Staff
from user.administrator.serializers.role import RoleSerializer
from common.utils import validate_unique_phone, validate_unique_email
from academics.models import Faculty, Grade
from common.utils import to_internal_value
from django.db import transaction
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    full_name = serializers.CharField(write_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("id", "phone", "full_name", "email", "first_name", "last_name")


class StaffSerializer(serializers.ModelSerializer):
    photo = serializers.CharField()
    designation__name = serializers.CharField(read_only=True)
    user = UserSerializer()

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res["roles"] = RoleSerializer(
            instance.user.roles.all().values("id", "title"), many=True
        ).data
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
        ]

    def validate(self, attrs):
        compare_date = date.today().year - attrs["dob"].year
        if compare_date < 15:
            raise serializers.ValidationError("age should be greater than 15")
        return attrs

    def validate_user(self, user):
        """check that faculty name is already exist"""
        phone = user.get("phone")
        email = user.get("email")
        # phone number between 10 to 15
        if len(phone) < 10 or len(phone) > 15:
            raise serializers.ValidationError("enter the correct phone number!")
        # validate unique ph numbers
        if phone:
            phone = validate_unique_phone(
                User, phone, self.context.get("institution"), self.instance
            )
        if email:
            email = validate_unique_email(
                User, email, self.context.get("institution"), self.instance
            )
        return user

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data.pop("user")
        photo = validated_data.pop("photo")
        full_name = user["full_name"].strip().split()
        first_name, last_name = full_name[0], full_name[1:]
        last_name_all = " ".join(last_name)
        user = User.objects.create(
            phone=user.get("phone"),
            first_name=first_name,
            email=user.get("email"),
            last_name=last_name_all,
            institution=self.context.get("institution"),
        )
        staff = Staff.objects.create(
            user=user, photo=to_internal_value(photo), **validated_data
        )
        return staff

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        users_obj = self.instance.user
        userSerializer = UserSerializer(users_obj, data=user_data, partial=True)
        if userSerializer.is_valid(raise_exception=True):
            full_name = userSerializer.validated_data["full_name"].strip().split()
            first_name, last_name = full_name[0], full_name[1:]
            userSerializer.save()
            last_name_all = " ".join(last_name)
            user_data_obj = User.objects.get(id=self.instance.user.id)
            user_data_obj.first_name = first_name
            user_data_obj.last_name = last_name_all
            user_data_obj.save()
        super(StaffSerializer, self).update(instance, validated_data)
        return instance


class StaffListSerializer(serializers.ModelSerializer):
    designation__name = serializers.CharField(read_only=True)
    staff_contact_number = serializers.CharField(read_only=True)
    staff_email = serializers.CharField(read_only=True)
    staff_first_name = serializers.CharField(read_only=True)
    staff_last_name = serializers.CharField(read_only=True)
    gender_name = serializers.CharField(source="get_gender_display", read_only=True)
    religion_name = serializers.CharField(source="get_religion_display", read_only=True)
    blood_group_name = serializers.CharField(
        source="get_blood_group_display", read_only=True
    )

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res["user"] = UserSerializer(instance.user).data
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
            "staff_contact_number",
            "staff_email",
            "staff_first_name",
            "staff_last_name",
            "user",
        ]


class StaffAssignSerialzer(serializers.ModelSerializer):
    phone = serializers.CharField()
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return obj.roles.all().values("title")

    class Meta:
        model = User
        fields = ("id", "phone", "roles")
