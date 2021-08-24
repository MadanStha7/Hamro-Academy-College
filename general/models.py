from django.db import models
from common.models import CommonInfo
from academics.models import Grade

# Create your models here.


class AcademicSession(CommonInfo):
    """
    model to store the academic session of college
    """

    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name="academic_session",
    )
    name = models.CharField(max_length=60)
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "Academic Session"
        ordering = ["-created_on"]

    def __str__(self):
        return self.name



    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(AcademicSession, self).save(*args, **kwargs)
