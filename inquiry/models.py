from django.db import models
from common.models import CommonInfo
from common.constant import SELECT_GENDER, SELECT_MARK_TYPE
from academics.models import Faculty


class Inquiry(CommonInfo):
    """
    Model to store the inquiry of parents for the front desk offcier
    """

    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=25)
    gender = models.CharField(max_length=1, choices=SELECT_GENDER)
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name="inquiry"
    )
    contact_number = models.CharField(max_length=25)
    email = models.EmailField(max_length=50, null=True, blank=True)
    previous_school = models.CharField(max_length=80, null=True, blank=True)
    marks_type = models.CharField(
        max_length=1, choices=SELECT_MARK_TYPE, null=True, blank=True
    )
    marks_obtained = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.0, blank=True
    )
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Inquiry"
        ordering = ["-created_on"]

    def __str__(self):
        return f"Inquiry made by {self.first_name} in  {self.institution}"
