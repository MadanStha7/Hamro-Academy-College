from django.db import models

from academics.models import Faculty, Grade
from common.models import CommonInfo


class FeeType(CommonInfo):
    """
    model to store the fee type
    """

    name = models.CharField(max_length=64)
    faculty = models.ManyToManyField(Faculty, related_name="fee_type")
    grade = models.ManyToManyField(Grade, related_name="fee_type")
    due_date = models.DateField()

    def __str__(self):
        return "{} -- {}".format(self.name, self.institution)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(FeeType, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_on"]
        db_table = "fee_type"
