# Generated by Django 3.2.5 on 2021-07-31 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("guardian", "0001_initial"),
        (
            "student",
            "0002_previousacademicdetail_studentacademicdetail_studentcategory_studentdocument_studentinfo",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="studentguardianinfo",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="studentguardianinfo",
            name="institution",
        ),
        migrations.RemoveField(
            model_name="studentguardianinfo",
            name="modified_by",
        ),
        migrations.RemoveField(
            model_name="studentguardianinfo",
            name="secondary_guardian",
        ),
        migrations.RemoveField(
            model_name="studentguardianinfo",
            name="user",
        ),
        migrations.AlterField(
            model_name="studentinfo",
            name="guardian_detail",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="student_info",
                to="guardian.studentguardianinfo",
            ),
        ),
        migrations.AlterModelTable(
            name="studentcategory",
            table="students_category",
        ),
        migrations.DeleteModel(
            name="SecondaryGuardianInfo",
        ),
        migrations.DeleteModel(
            name="StudentGuardianInfo",
        ),
    ]