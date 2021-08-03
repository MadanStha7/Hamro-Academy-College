from django.db import models

from django.conf import settings

from core.models import InstitutionInfo
from uuid import uuid4


class SystemRole(models.TextChoices):
    STUDENT = "Student"
    ADMINISTRATOR = "Administrator"
    TEACHER = "Teacher"
    PARENT = "Parent"
    FRONT_DESK_OFFICER = "Front Desk Officer"


class CommonInfo(models.Model):
    """
    common info that is frequently to be used in every model
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    institution = models.ForeignKey(
        InstitutionInfo,
        related_name="%(app_label)s_%(class)s_general_info",
        on_delete=models.PROTECT,
    )
    created_on = models.DateTimeField("Created at", auto_now_add=True, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Created by",
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.PROTECT,
    )
    modified_on = models.DateTimeField("Last modified at", auto_now=True, db_index=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Modified by",
        related_name="%(app_label)s_%(class)s_modified",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
