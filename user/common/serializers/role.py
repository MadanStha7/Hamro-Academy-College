import uuid
from rest_framework import serializers
from user.models import Role
from django.db import transaction
from django.contrib.auth.models import Group
from common.utils import validate_unique_role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ["institution"]
        model = Role
        fields = ("id", "title", "description", "institution")

    def validate_title(self, title):
        """check that faculty name is already exist"""
        print("institution", self.context.get("institution"))
        title = validate_unique_role(
            Role, title, self.context.get("institution"), self.instance
        )
        return title

    @transaction.atomic
    def create(self, validated_data):
        id_ = uuid.uuid4()
        group = Group.objects.create(name=str(id_))
        group.save()
        role = Role.objects.create(group=group, **validated_data)
        return role
