from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers
from common.constant import SYSTEM_DEFAULT_PASSWORD
from common.utils import to_internal_value
from guardian.models import SecondaryGuardianInfo, StudentGuardianInfo
from user.common.serializers.user import UserSerializer
from user.models import SystemUser

User = get_user_model()


class SecondaryGuardianInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryGuardianInfo
        read_only_fields = ["photo"]
        fields = ["id", "relation", "full_name", "address", "phone", "photo"]


class GuardianInfoSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField(
        read_only=True, required=False, allow_null=True
    )
    user = UserSerializer()

    def get_photo(self, obj):
        return obj.photo.url if obj.photo else None

    class Meta:
        model = StudentGuardianInfo
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "user",
            "address",
            "relation",
            "photo",
            "phone",
            "occupation",
            "institution",
            "created_by",
        ]

    def create(self, validated_data):
        user = validated_data.pop("user")
        photo = validated_data.pop("photo")
        user["institution"] = validated_data.get("institution")
        user = SystemUser(**user)
        user.save()
        validated_data["user"] = user
        guardian_info = StudentGuardianInfo.objects.create(**validated_data)
        if photo:
            guardian_info.photo = to_internal_value(photo)
        guardian_info.save()
        return guardian_info

    @transaction.atomic()
    def update(self, instance, validated_data):
        photo = validated_data.pop("photo")
        if validated_data.get("user"):
            user_update = UserSerializer(
                data=validated_data.pop("user"),
                instance=instance.user,
            )
            user_update.is_valid(raise_exception=True)
            user_update.save()
        if photo:
            instance.photo = to_internal_value(photo)
            instance.save()
        return super(GuardianInfoSerializer, self).update(instance, validated_data)


class StudentGuardianInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StudentGuardianInfo
        read_only_fields = ["photo", "institution", "created_by"]
        fields = [
            "id",
            "user",
            "address",
            "relation",
            "photo",
            "phone",
            "occupation",
            "institution",
            "created_by",
        ]
