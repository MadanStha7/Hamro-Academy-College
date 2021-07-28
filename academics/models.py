from django.db import models
from common.models import CommonInfo
from common.constant import GRADE_CHOICES


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
