# Generated by Django 3.2.5 on 2021-08-25 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemuser',
            name='middle_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='middle name'),
        ),
    ]
