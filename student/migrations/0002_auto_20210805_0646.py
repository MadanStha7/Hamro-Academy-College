# Generated by Django 3.2.5 on 2021-08-05 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentinfo',
            name='marital_status',
        ),
        migrations.RemoveField(
            model_name='studentinfo',
            name='spouse_name',
        ),
    ]
