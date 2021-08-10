# Generated by Django 3.2.5 on 2021-08-10 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
        ('academics', '0003_auto_20210810_0603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineclassinfo',
            name='academic_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='online_class_info', to='general.academicsession'),
        ),
        migrations.AlterField(
            model_name='onlineclassinfo',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='online_class_info', to='academics.faculty'),
        ),
        migrations.AlterField(
            model_name='onlineclassinfo',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='online_class_info', to='academics.grade'),
        ),
        migrations.AlterField(
            model_name='onlineclassinfo',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='online_class_info', to='academics.section'),
        ),
        migrations.AlterField(
            model_name='onlineclassinfo',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='online_class_info', to='academics.subject'),
        ),
    ]