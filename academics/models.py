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
        return super(Section, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Subject(CommonInfo):
    """
    model to store subjects
    """

    SUBJECT_TYPES = (("1", "Theory"), ("2", "Practical"), ("3", "Theory and Practical"))

    name = models.CharField(max_length=50)
    credit_hour = models.FloatField()
    subject_code = models.CharField(max_length=10)
    subject_type = models.CharField(max_length=1, choices=SUBJECT_TYPES)

    class Meta:
        db_table = "academics_subject"
        unique_together = ["name", "institution"]

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class SubjectGroup(CommonInfo):
    name = models.CharField(max_length=50)
    section = models.ManyToManyField(Section, related_name="subject_group", blank=True)
    grade = models.ForeignKey(
        Grade, related_name="subject_group", on_delete=models.CASCADE
    )
    faculty = models.ForeignKey(
        Faculty, related_name="subject_group", on_delete=models.CASCADE
    )
    subject = models.ManyToManyField(Subject, related_name="subjects")
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "academics_subject_group"
        unique_together = ["name", "institution"]

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(SubjectGroup, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
