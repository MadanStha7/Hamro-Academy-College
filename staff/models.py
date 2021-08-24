from django.db import models
from django.contrib.auth import get_user_model
from common.models import CommonInfo
from common.constant import (
    SELECT_RELIGION,
    SELECT_GENDER,
    SELECT_BLOOD_GROUP,
    CONTRACT_TYPE,
    SELECT_MARITAL_STATUS,
)
from academics.models import Faculty, Shift

User = get_user_model()


class Designation(CommonInfo):
    """
    model to store the desingation of staff
    """

    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(Designation, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_on"]
        db_table = "designation"


class Staff(CommonInfo):
    """
    model to store the staff detail
    """

    photo = models.ImageField(
        upload_to="staff_photo/", default="default_images/default_profile_pic.png"
    )
    user = models.OneToOneField(User, related_name="staff", on_delete=models.CASCADE)
    designation = models.ForeignKey(
        Designation,
        related_name="staff",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    address = models.TextField()
    dob = models.DateField()
    marital_status = models.CharField(max_length=1, choices=SELECT_MARITAL_STATUS)
    spouse_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):

        return "{} -- {}".format(self.user.email, self.institution)

    class Meta:
        db_table = "staff"
        ordering = ["-created_on"]


class StaffAcademicInfo(CommonInfo):
    """
    model to store the staff additional detail
    """

    staff = models.OneToOneField(
        Staff, related_name="staff_academic_info", on_delete=models.CASCADE
    )
    shift = models.ManyToManyField(Shift, related_name="staff_academic_info_faculty")
    faculty = models.ManyToManyField(Faculty, related_name="staff_academic_info_shift")
    highest_degree = models.CharField(max_length=50, null=True, blank=True)
    experience = models.FloatField(default=0, null=True, blank=True)
    working_days = models.IntegerField(null=True, blank=True)
    leave = models.FloatField(
        default=0, help_text="Staff's leave days", null=True, blank=True
    )
    previous_academic_details = models.BooleanField(default=False)
    previous_college_name = models.CharField(max_length=40, null=True, blank=True)
    previous_college_email = models.EmailField(max_length=40, null=True, blank=True)
    previous_college_contact = models.CharField(max_length=40, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "staff_academic_info"
        ordering = ["created_on"]


class Document(CommonInfo):
    """
    model to store the document of staff
    """

    staff = models.ForeignKey(Staff, related_name="documents", on_delete=models.CASCADE)
    document = models.FileField(upload_to="staff/document_upload/")
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "staff_document"
        ordering = ["-created_on"]
