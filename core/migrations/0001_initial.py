# Generated by Django 3.2.5 on 2021-07-26 08:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="InstitutionInfo",
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
                ("logo", models.ImageField(blank=True, null=True, upload_to="logo/")),
                ("name", models.CharField(max_length=50)),
                ("abbreviation", models.CharField(max_length=10)),
                ("address", models.TextField()),
                ("phone_number", models.CharField(max_length=15)),
                ("email", models.EmailField(max_length=254)),
                ("slogan", models.TextField()),
                ("reg_number", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "institution_name",
            },
        ),
    ]
