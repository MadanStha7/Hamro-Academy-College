# Generated by Django 3.2.5 on 2021-08-18 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
        ('academics', '0006_delete_onlineclassinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeeType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('modified_on', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last modified at')),
                ('name', models.CharField(max_length=64)),
                ('due_date', models.DateField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fees_feetype_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('faculty', models.ManyToManyField(related_name='fee_type', to='academics.Faculty')),
                ('grade', models.ManyToManyField(related_name='fee_type', to='academics.Grade')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fees_feetype_general_info', to='core.institutioninfo')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fees_feetype_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
            ],
            options={
                'db_table': 'fee_type',
                'ordering': ['-created_on'],
            },
        ),
    ]
