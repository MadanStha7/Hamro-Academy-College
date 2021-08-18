from django.contrib.postgres.fields import ArrayField
from django.db import models
from academics.models import Subject, Grade, Section, Faculty
from common.constant import DAY
from common.models import CommonInfo
from student.models import StudentAcademicDetail


class OnlineClassInfo(CommonInfo):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="online_class_info",
        db_index=True,
    )
    class_date = models.DateField(null=True, blank=True)
    days = ArrayField(
        models.CharField(max_length=1, choices=DAY), default=list, blank=True, null=True
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    grade = models.ForeignKey(
        Grade, related_name="online_class_info", on_delete=models.CASCADE, db_index=True
    )
    section = models.ForeignKey(
        Section,
        related_name="online_class_info",
        on_delete=models.CASCADE,
        db_index=True,
        blank=True,
        null=True,
    )
    faculty = models.ForeignKey(
        Faculty, related_name="online_class_info", on_delete=models.CASCADE
    )
    academic_session = models.ForeignKey(
        "general.AcademicSession",
        on_delete=models.CASCADE,
        related_name="online_class_info",
    )
    link_code = models.CharField(max_length=253)
    is_regular = models.BooleanField(default=False)

    class Meta:
        db_table = "online_class"
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title}"


class StudentOnlineClassAttendance(CommonInfo):
    online_class = models.ForeignKey(
        OnlineClassInfo,
        related_name="student_online_class_attendance",
        on_delete=models.CASCADE,
    )
    student_academic = models.ForeignKey(
        StudentAcademicDetail,
        related_name="student_online_class_attendance",
        on_delete=models.CASCADE,
    )
    joined_on = models.TimeField()

    def __str__(self):
        return self.online_class.link_code

    class Meta:
        db_table = "student_online_class_attendance"
        ordering = ["-created_on"]
