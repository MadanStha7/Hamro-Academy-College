from django.db import models
from django.apps import apps
from django.contrib.auth.hashers import make_password
from common.models import SystemRole
from django.contrib.auth.models import AbstractUser, Group
from uuid import uuid4
from django.contrib.auth.models import Permission, GroupManager, UserManager
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


class SystemUserManager(UserManager):
    def _create_user(self, phone, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone:
            raise ValueError("The given phone must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        phone = GlobalUserModel.normalize_username(phone)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, email, password, **extra_fields)

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(phone, email, password, **extra_fields)


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
    phone = models.CharField(max_length=15, unique=True)
    username = None
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
    USERNAME_FIELD = "phone"
    objects = SystemUserManager()
