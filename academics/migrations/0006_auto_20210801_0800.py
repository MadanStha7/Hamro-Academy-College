from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0002_alter_institutioninfo_table"),
        ("academics", "0005_merge_20210730_0856"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shift",
            name="name",
            field=models.CharField(
                choices=[
                    ("Morning", "Morning"),
                    ("Day", "Day"),
                    ("Evening", "Evening"),
                    ("Extra", "Extra"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="subject",
            unique_together=set(),
        ),
        migrations.CreateModel(
            name="ApplyShift",
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
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="academics_applyshift_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "faculty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="apply_shift",
                        to="academics.faculty",
                    ),
                ),
                (
                    "grade",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="apply_shift",
                        to="academics.grade",
                    ),
                ),
                (
                    "institution",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="academics_applyshift_general_info",
                        to="core.institutioninfo",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="academics_applyshift_modified",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modified by",
                    ),
                ),
                (
                    "section",
                    models.ManyToManyField(
                        blank=True, related_name="apply_shift", to="academics.Section"
                    ),
                ),
                (
                    "shift",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="apply_shift",
                        to="academics.shift",
                    ),
                ),
            ],
            options={
                "db_table": "academic_apply_shift",
            },
        ),
    ]
