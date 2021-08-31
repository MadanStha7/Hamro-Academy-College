from django.db import models
from django.contrib.auth import get_user_model
from common.models import CommonInfo

from common.constant import (
    RELATION_STATUS_CHOICES,
)

User = get_user_model()


class SecondaryGuardianInfo(CommonInfo):
    relation = models.CharField(max_length=1, choices=RELATION_STATUS_CHOICES)
    full_name = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField(max_length=15, db_index=True)
    photo = models.ImageField(
        upload_to="secondary_guardian/images",
        default="default_images/default_profile_pic.png",
    )

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "secondary_guardians_info"
        ordering = ["-created_on"]


class StudentGuardianInfo(CommonInfo):
    user = models.ForeignKey(
        User, related_name="student_guardian_info", on_delete=models.CASCADE
    )
    occupation = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField()
    photo = models.ImageField(
        upload_to="parent/images", default="default_images/default_profile_pic.png"
    )
    relation = models.CharField(max_length=1, choices=RELATION_STATUS_CHOICES)
    secondary_guardian = models.ForeignKey(
        SecondaryGuardianInfo,
        on_delete=models.CASCADE,
        related_name="student_secondary_guardian",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.get_full_name()}"

    class Meta:
        db_table = "students_guardian_info"
        ordering = ["-created_on"]
