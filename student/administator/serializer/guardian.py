from django.db import transaction

from common.constant import SYSTEM_DEFAULT_PASSWORD
from student.models import StudentGuardianInfo, SecondaryGuardianInfo
from rest_framework import serializers


from django.contrib.auth import get_user_model

from user.administrator.serializers.user import UserSerializer

User = get_user_model()


class SecondaryGuardianInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryGuardianInfo
        read_only_fields = ["photo"]
        fields = ["id", "relation", "full_name", "address", "phone", "photo"]


class GuardianListInfoSerializer(serializers.ModelSerializer):
    """
    serializer to list the guardian info of student
    """

    user = UserSerializer()
    secondary_id = serializers.IntegerField()
    secondary_full_name = serializers.CharField()
    secondary_address = serializers.CharField()
    secondary_phone = serializers.CharField()

    class Meta:
        model = StudentGuardianInfo
        read_only_fields = ["photo"]
        fields = [
            "id",
            "photo",
            "user",
            "address",
            "phone",
            "secondary_id",
            "secondary_full_name",
            "secondary_address",
            "secondary_phone",
        ]


class GuardianInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    secondary_guardian = SecondaryGuardianInfoSerializer(required=False)

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
            "secondary_guardian",
            "institution",
            "created_by",
        ]

    def create(self, validated_data):
        secondary_guardian_data = None
        user = validated_data.pop("user")
        user["institution"] = validated_data.get("institution")
        secondary_guardian = validated_data.pop("secondary_guardian", {})
        if secondary_guardian:
            serializer = SecondaryGuardianInfoSerializer(data=secondary_guardian)
            if serializer.is_valid():
                secondary_guardian_data = serializer.save(
                    institution=validated_data.get("institution"),
                    created_by=validated_data.get("created_by"),
                )
        user = User(**user, username=validated_data.get("phone"))
        user.set_password(SYSTEM_DEFAULT_PASSWORD)
        user.save()
        validated_data["user"] = user
        guardian_info = StudentGuardianInfo.objects.create(**validated_data)
        if secondary_guardian_data:
            guardian_info.secondary_guardian = secondary_guardian_data
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

        if validated_data.get("secondary_guardian"):
            secondary_guardian_json_data = validated_data.pop("secondary_guardian")
            # if instance.secondary_guardian:
            (
                secondary_guardian,
                created,
            ) = SecondaryGuardianInfo.objects.update_or_create(
                id=instance.secondary_guardian.id if instance.secondary_guardian else 0,
                defaults={
                    "full_name": secondary_guardian_json_data.get("full_name"),
                    "relation": secondary_guardian_json_data.get("relation"),
                    "address": secondary_guardian_json_data.get("address"),
                    "phone": secondary_guardian_json_data.get("phone"),
                    "institution": instance.institution,
                    "created_by": instance.created_by,
                },
            )

            instance.secondary_guardian = secondary_guardian

        return super(GuardianInfoSerializer, self).update(instance, validated_data)
