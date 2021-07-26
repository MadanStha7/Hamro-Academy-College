from django.contrib import admin
from .models import SystemUser

# Register your models here.
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = "__all__"


class SystemUserAdmin(UserAdmin):
    readonly_fields = ["password"]
    filter_horizontal = ("groups", "user_permissions", "roles")
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    ordering = ("-date_joined",)
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "roles",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Extended Fields"), {"fields": ("institution",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "institution"),
            },
        ),
    )
    form = CustomUserChangeForm


admin.site.register(SystemUser, SystemUserAdmin)
