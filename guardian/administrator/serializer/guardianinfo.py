from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers
from common.utils import validate_unique_phone, to_internal_value
from guardian.models import StudentGuardianInfo
from staff.administrator.serializers.staff import UserSerializer

User = get_user_model()


class GuardianInfoSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    photo = serializers.SerializerMethodField(read_only=True, required=False, allow_null=True)

    def get_photo(self, obj):
        return obj.photo.url if obj.photo else None

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
        # phone number between 7 to 14
        if len(phone) < 7 or len(phone) > 14:
            raise serializers.ValidationError("length of phone number should be more than 10 and less than 14!")
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
            guardian = StudentGuardianInfo.objects.create(user=user, **validated_data)
            if photo:
                guardian.photo = to_internal_value(photo)
                guardian.save()

            return guardian

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


