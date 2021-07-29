import uuid
from user.models import Role
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.db import transaction
from common.utils import validate_unique_role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ["institution"]
        model = Role
        fields = ["id", "title", "description", "institution"]

    def validate_title(self, title):
        """check that faculty title is already exist"""
        title = validate_unique_role(
            Role, title, self.context.get("institution"), self.instance
        )
        return title

    @transaction.atomic
    def create(self, validated_data):
        token = uuid.uuid4()
        group = Group.objects.create(name=str(token))
        group.save()
        role = Role.objects.create(group=group, **validated_data)
        return role

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        return instance
