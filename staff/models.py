from django.db import models
from django.contrib.auth import get_user_model
from common.models import CommonInfo
from common.constant import (
    SELECT_RELIGION,
    SELECT_GENDER,
    SELECT_BLOOD_GROUP,
    CONTRACT_TYPE,
)
from academics.models import Faculty

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
        Designation, related_name="staff", on_delete=models.CASCADE
    )
    faculty = models.ManyToManyField(Faculty, related_name="staff")
    address = models.TextField()
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=SELECT_GENDER)
    religion = models.CharField(
        max_length=30, choices=SELECT_RELIGION, blank=True, null=True
    )
    blood_group = models.CharField(max_length=1, choices=SELECT_BLOOD_GROUP)
    pan_no = models.CharField(max_length=50)
    date_of_joining = models.DateField()

    def __str__(self):
        return f"{self.user.get_full_name()}-{self.institution.name}"

    class Meta:
        db_table = "staff"
        ordering = ["-created_on"]


class StaffAcademicInfo(CommonInfo):
    """
    model to store the staff additional detail
    """

    contract_type = models.CharField(max_length=1, choices=CONTRACT_TYPE)
    staff = models.OneToOneField(
        Staff, related_name="staff_academic_info", on_delete=models.CASCADE
    )
    highest_degree = models.CharField(max_length=50)
    experience = models.FloatField(default=0)
    working_days = models.IntegerField()
    leave = models.FloatField(default=0, help_text="Staff's leave days")

    def __str__(self):
        return self.staff.phone

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
        return self.staff.user.username

    class Meta:
        db_table = "staff_document"
        ordering = ["-created_on"]
