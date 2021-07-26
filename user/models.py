from django.db import models
from common.models import SystemRole
from django.contrib.auth.models import AbstractUser, Group
from uuid import uuid4
from django.contrib.auth.models import Permission, GroupManager
from core.models import InstitutionInfo
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    group = models.OneToOneField(
        Group, related_name="%(app_label)s_%(class)s_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=63, choices=SystemRole.choices)
    description = models.CharField(max_length=63, null=True, blank=True)
    institution = models.ForeignKey(
        InstitutionInfo, on_delete=models.CASCADE, related_name="roles"
    )

    def __str__(self):
        return f"{self.title} - {self.institution.name}"

    class Meta:
        db_table = "role"
        unique_together = ["title", "institution"]


class SystemUser(AbstractUser):
    """
    extending the user info with general info as external field
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    institution = models.ForeignKey(
        InstitutionInfo,
        related_name="user_general_info",
        on_delete=models.CASCADE,
        help_text="Choose the institution current user belongs to",
        null=True,
        blank=True,
    )
    phone = models.CharField(max_length=15)
    roles = models.ManyToManyField(
        Role,
        verbose_name=_("roles"),
        blank=True,
        help_text=_(
            "The role this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_roles",
        related_query_name="roles",
    )
