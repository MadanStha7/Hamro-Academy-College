# Generated by Django 3.2.5 on 2021-08-31 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guardian', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentguardianinfo',
            name='phone',
        ),
    ]
