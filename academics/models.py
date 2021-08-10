from django.contrib.postgres.fields import ArrayField
from django.db import models
from common.models import CommonInfo
from common.constant import GRADE_CHOICES, SUBJECT_TYPES, SHIFT_CHOICES, DAY


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
        return f"{self.institution}-{self.name}"


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


class Subject(CommonInfo):
    """
    model to store subjects
    """

    name = models.CharField(max_length=50)
    credit_hour = models.FloatField()
    subject_code = models.CharField(max_length=10)
    subject_type = models.CharField(max_length=1, choices=SUBJECT_TYPES)

    class Meta:
        db_table = "academics_subjects"

    def save(self, *args, **kwargs):
        self.name = self.name.title()

        return super(Subject, self).save(*args, **kwargs)


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
        db_table = "academic_subject_group"
        unique_together = ["name", "institution"]

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(SubjectGroup, self).save(*args, **kwargs)

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


class ApplyShift(CommonInfo):
    shift = models.ForeignKey(Shift, related_name="apply_shift", on_delete=models.CASCADE)
    grade = models.ForeignKey(
        Grade, related_name="apply_shift", on_delete=models.CASCADE
    )
    section = models.ForeignKey(Section, related_name="apply_shift", on_delete=models.CASCADE, blank=True, null=True)
    faculty = models.ForeignKey(
        Faculty, related_name="apply_shift", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "academic_apply_shift"
        unique_together = ["shift", "grade", "section", "faculty", "institution"]

    def __str__(self):
        return f"{self.shift.name}"


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

    class Meta:
        db_table = "online_class"
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.grade}"
