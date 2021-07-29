# Generated by Django 3.2.5 on 2021-07-28 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("academics", "0002_faculty"),
        ("general", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="academicsession",
            name="grade",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="academic_session",
                to="academics.grade",
            ),
            preserve_default=False,
        ),
    ]
