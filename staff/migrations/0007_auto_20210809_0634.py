# Generated by Django 3.2.5 on 2021-08-09 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "staff",
            "0006_rename_previouse_academic_details_staffacademicinfo_previous_academic_details",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="staffacademicinfo",
            name="previous_contact",
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name="staffacademicinfo",
            name="previous_email",
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]