from django.db import models
from django.db.models.fields.related import ForeignKey
from common.models import CommonInfo
from common.constant import GRADE_CHOICES, SHIFT_CHOICES


class Section(CommonInfo):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "academics_section"
        unique_together = ["name", "institution"]

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(Section, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Grade(CommonInfo):

    name = models.CharField(max_length=20, choices=GRADE_CHOICES)

    class Meta:
        db_table = "academics_grade"
        unique_together = ["name", "institution"]

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(Grade, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Faculty(CommonInfo):
    """
    model to store the faculty
    """

    name = models.CharField(max_length=50)

    class Meta:
        db_table = "academics_faculty"
        unique_together = ["name", "institution"]

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(Faculty, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Shift(CommonInfo):
    name = models.CharField(choices=SHIFT_CHOICES, max_length=50)
    faculty = models.ForeignKey(
        Faculty, related_name="faculty_shift", on_delete=models.CASCADE
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = "academics_shift"
        unique_together = ["name", "institution"]

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(Shift, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Class(CommonInfo):
    faculty = models.ForeignKey(
        Faculty, related_name="class_faculty", on_delete=models.CASCADE
    )
    grade = models.ForeignKey(
        Grade, related_name="class_grade", on_delete=models.CASCADE
    )
    section = models.ManyToManyField(Section, related_name="class_section", blank=True)

    class Meta:
        db_table = "academics_class"

    def __str__(self):
        return f"{self.faculty.name}"
