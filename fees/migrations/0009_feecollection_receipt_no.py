# Generated by Django 3.2.5 on 2021-09-15 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fees", "0008_auto_20210912_1029"),
    ]

    operations = [
        migrations.AddField(
            model_name="feecollection",
            name="receipt_no",
            field=models.CharField(
                help_text="Receipt ID of the student fee payment",
                max_length=31,
                null=True,
            ),
        ),
    ]
