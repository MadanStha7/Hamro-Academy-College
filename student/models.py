from django.db import models
from django.contrib.auth import get_user_model

from academics.models import Grade, Section, Faculty, Shift
from common.models import CommonInfo

from common.constant import (
    RELATION_STATUS_CHOICES,
    SELECT_GENDER,
    SELECT_MARITAL_STATUS,
)
from general.models import AcademicSession

User = get_user_model()


class SecondaryGuardianInfo(CommonInfo):
    relation = models.CharField(max_length=1, choices=RELATION_STATUS_CHOICES)
    full_name = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField(max_length=15, db_index=True)
    photo = models.ImageField(
        upload_to="secondary_guardian/images",
        default="default_images/default_profile_pic.png",
    )

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "secondary_guardian_info"
        ordering = ["-created_on"]


class StudentGuardianInfo(CommonInfo):
    user = models.ForeignKey(
        User, related_name="student_guardian_info", on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=15, unique=True, db_index=True)
    occupation = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField()
    photo = models.ImageField(
        upload_to="parent/images", default="default_images/default_profile_pic.png"
    )
    email = models.EmailField()
    relation = models.CharField(max_length=1, choices=RELATION_STATUS_CHOICES)
    secondary_guardian = models.ForeignKey(
        SecondaryGuardianInfo,
        on_delete=models.CASCADE,
        related_name="student_secondary_guardian",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.get_full_name()}"

    class Meta:
        db_table = "student_guardian_info"
        ordering = ["-created_on"]


class StudentCategory(CommonInfo):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "student_category"


class StudentInfo(CommonInfo):
    admission_number = models.CharField(max_length=20)
    user = models.OneToOneField(
        User, related_name="student_info", on_delete=models.CASCADE
    )
    temporary_address = models.TextField()
    permanent_address = models.TextField()
    student_category = models.ForeignKey(
        StudentCategory,
        related_name="student_info",
        on_delete=models.CASCADE,
    )
    guardian_detail = models.ForeignKey(
        StudentGuardianInfo,
        related_name="student_info",
        on_delete=models.CASCADE,
    )
    phone = models.CharField(max_length=15, db_index=True)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=SELECT_GENDER)
    photo = models.ImageField(upload_to="student-photos/")
    marital_status = models.CharField(max_length=1, choices=SELECT_MARITAL_STATUS)
    spouse_name = models.CharField(max_length=20, null=True, blank=True)

    disable = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"{self.admission_number}"

    class Meta:
        ordering = ["-created_on"]
        db_table = "student_students_admission"


class StudentDocument(CommonInfo):
    student = models.ForeignKey(
        StudentInfo, related_name="student_document", on_delete=models.CASCADE
    )
    document = models.FileField(upload_to="student/document/")
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.get_first_name()}"

    class Meta:
        db_table = "student_document"


class PreviousAcademicDetail(CommonInfo):
    student = models.ForeignKey(
        StudentInfo, related_name="previous_academic_detail", on_delete=models.CASCADE
    )
    last_school = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField(max_length=15, db_index=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        db_table = "previous_academic_info"


class StudentAcademicDetail(CommonInfo):
    student = models.ForeignKey(
        StudentInfo, related_name="student_academic_detail", on_delete=models.PROTECT
    )
    grade = models.ForeignKey(
        Grade, related_name="student_academic_detail", on_delete=models.CASCADE
    )
    section = models.ForeignKey(
        Section,
        related_name="student_academic_detail",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    faculty = models.ForeignKey(
        Faculty, related_name="student_academic", on_delete=models.CASCADE
    )
    shift = models.ForeignKey(
        Shift,
        related_name="student_academic",
        on_delete=models.CASCADE,
    )
    academic_session = models.ForeignKey(
        AcademicSession,
        related_name="student_academic_detail",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"{self.student.user.get_first_name()}"

    class Meta:
        db_table = "student_academic"
