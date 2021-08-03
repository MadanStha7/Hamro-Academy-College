from rest_framework import serializers
from staff.models import Staff
from common.utils import validate_unique_phone
from django.db import transaction
from django.contrib.auth import get_user_model
from academics.models import Faculty, Grade

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    full_name = serializers.CharField(write_only=True)
    user_full_name = serializers.SerializerMethodField(read_only=True)

    def get_user_full_name(self, obj):
        name = obj.first_name + " " + obj.last_name
        return name

    class Meta:
        model = User
        read_only_fields = ["first_name", "last_name"]

        fields = ("id", "phone", "full_name", "user_full_name")


class StaffSerializer(serializers.ModelSerializer):
    designation__name = serializers.CharField(read_only=True)
    faculty_name = serializers.StringRelatedField(
        many=True, read_only=True, source="faculty"
    )
    gender_name = serializers.CharField(source="get_gender_display", read_only=True)
    gender_name = serializers.CharField(source="get_gender_display", read_only=True)
    religion_name = serializers.CharField(source="get_religion_display", read_only=True)
    blood_group_name = serializers.CharField(
        source="get_blood_group_display", read_only=True
    )
    user = UserSerializer()

    class Meta:
        model = Staff
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "photo",
            "user",
            "designation",
            "address",
            "phone",
            "dob",
            "gender",
            "religion",
            "blood_group",
            "pan_no",
            "date_of_joining",
            "designation__name",
            "gender_name",
            "religion_name",
            "blood_group_name",
            "faculty",
            "faculty_name",
        ]

    def validate(self, attrs):
        """
        check if the faculty is same
        """
        no_of_faculty = []
        for item in attrs["faculty"]:
            no_of_faculty.append(item)

        for value in no_of_faculty:
            if no_of_faculty.count(value) > 1:
                raise serializers.ValidationError("Same Faculty cannot be selected!")
        return attrs

    def validate_user(self, user):
        """check that faculty name is already exist"""
        phone = user.get("phone")
        phone = validate_unique_phone(
            User, phone, self.context.get("institution"), self.instance
        )
        return user

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data.pop("user")
        faculty_data = validated_data.pop("faculty")
        for element in faculty_data:
            faculty_id = element.id
        all_name = user["full_name"].strip().split()
        first_name, last_name = all_name[0], all_name[1:]
        last_name_all = " ".join(last_name)
        user = User.objects.create(
            phone=user.get("phone"),
            first_name=first_name,
            last_name=last_name_all,
            institution=self.context.get("institution"),
        )
        staff = Staff.objects.create(user=user, **validated_data)
        staff.faculty.add(faculty_id)
        return staff

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        users_obj = self.instance.user
        faculty_data = validated_data.pop("faculty")
        instance.photo = validated_data.get("photo", instance.photo)
        instance.designation = validated_data.get("designation", instance.designation)
        instance.address = validated_data.get("address", instance.address)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.dob = validated_data.get("dob", instance.dob)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.religion = validated_data.get("religion", instance.religion)
        instance.blood_group = validated_data.get("blood_group", instance.blood_group)
        instance.pan_no = validated_data.get("pan_no", instance.pan_no)
        instance.pan_no = validated_data.get("pan_no", instance.pan_no)
        for faculty in faculty_data:
            instance.faculty.add(faculty)
        userSerializer = UserSerializer(users_obj, data=user_data, partial=True)
        if userSerializer.is_valid(raise_exception=True):
            all_name = userSerializer.validated_data["full_name"].strip().split()
            first_name, last_name = all_name[0], all_name[1:]
            userSerializer.save()
            last_name_all = " ".join(last_name)
            user_data_obj = User.objects.get(id=self.instance.user.id)
            user_data_obj.first_name = first_name
            user_data_obj.last_name = last_name_all
            user_data_obj.save()
        return instance
