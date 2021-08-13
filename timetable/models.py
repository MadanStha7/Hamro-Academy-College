from django.db import models
from common.models import CommonInfo
from common.constant import DAYS_CHOICES
from academics.models import Faculty, Grade, Shift, Section, Subject
from staff.models import Staff
from general.models import AcademicSession
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeTable(CommonInfo):
    """
    model to store the time table of regular class of student
    """

    day = models.PositiveSmallIntegerField(choices=DAYS_CHOICES)
    start_time = models.TimeField(help_text="starting time of class")
    end_time = models.TimeField(help_text="ending time of class")
    faculty = models.ForeignKey(
        Faculty,
        related_name="time_table",
        on_delete=models.CASCADE,
    )
    grade = models.ForeignKey(
        Grade,
        related_name="time_table",
        on_delete=models.CASCADE,
    )
    shift = models.ForeignKey(
        Shift,
        related_name="time_table",
        on_delete=models.CASCADE,
    )
    section = models.ForeignKey(
        Section,
        related_name="time_table_section",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    teacher = models.ForeignKey(
        User, related_name="time_table", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        related_name="time_table",
        on_delete=models.CASCADE,
    )
    academic_session = models.ForeignKey(
        AcademicSession,
        related_name="time_table",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "time_table"
        ordering = ["-id"]

    def __str__(self):
        return f"Time table of {str(self.id)}"
