# Generated by Django 3.2.5 on 2021-08-23 18:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("academics", "0006_delete_onlineclassinfo"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Inquiry",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                ("first_name", models.CharField(max_length=25)),
                ("middle_name", models.CharField(blank=True, max_length=20, null=True)),
                ("last_name", models.CharField(max_length=25)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female"), ("O", "Others")],
                        max_length=1,
                    ),
                ),
                ("contact_number", models.CharField(max_length=25)),
                (
                    "previous_school",
                    models.CharField(blank=True, max_length=80, null=True),
                ),
                (
                    "marks_type",
                    models.CharField(
                        blank=True,
                        choices=[("G", "GPA"), ("P", "PERCENTAGE")],
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "marks_obtained",
                    models.DecimalField(
                        blank=True, decimal_places=2, default=0.0, max_digits=6
                    ),
                ),
                ("remarks", models.TextField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="inquiry_inquiry_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "faculty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inquiry",
                        to="academics.faculty",
                    ),
                ),
                (
                    "institution",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="inquiry_inquiry_general_info",
                        to="core.institutioninfo",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="inquiry_inquiry_modified",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modified by",
                    ),
                ),
            ],
            options={
                "db_table": "Inquiry",
                "ordering": ["-created_on"],
            },
        ),
    ]
