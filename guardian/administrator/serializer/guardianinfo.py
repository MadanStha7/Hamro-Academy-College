from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers
from common.utils import validate_unique_phone
from guardian.models import StudentGuardianInfo
from user.common.serializers.user import UserSerializer


User = get_user_model()


class GuardianInfoSerializer(serializers.ModelSerializer):
    # photo = serializers.SerializerMethodField(
    #     read_only=True, required=False, allow_null=True
    # )
    user = UserSerializer()

    # def get_photo(self, obj):
    #     return obj.photo.url if obj.photo else None

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

    def validate_user(self, user):
        """check that faculty name is already exist"""
        phone = user.get("phone")
        # phone number between 10 to 15
        if len(phone) < 10 or len(phone) > 14:
            raise serializers.ValidationError("length of phone number should be more than 10 and less than 14!")
        phone = validate_unique_phone(
            User, phone, self.context.get("institution"), self.instance
        )
        return user

    def create(self, validated_data):
        user = validated_data.pop("user")
        guardian_serializer = UserSerializer(data=user)
        guardian_serializer.is_valid(raise_exception=True)
        user = guardian_serializer.save()
        user.general_info = validated_data.get("institution")
        guardian_info = StudentGuardianInfo.objects.create(**validated_data,
                                                           user=user)
        guardian_info.save()
        return guardian_info

    @transaction.atomic()
    def update(self, instance, validated_data):
        if validated_data.get("user"):
            user_update = UserSerializer(
                data=validated_data.pop("user"),
                instance=instance.user,
            )
            user_update.is_valid(raise_exception=True)
            user_update.save()
        return super(GuardianInfoSerializer, self).update(instance, validated_data)


