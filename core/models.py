from django.db import models
from uuid import uuid4


class InstitutionInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    logo = models.ImageField(upload_to="logo/", null=True, blank=True)
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=10)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    slogan = models.TextField()
    reg_number = models.CharField(max_length=50)

    class Meta:
        db_table = "institution"

    def __str__(self):
        return self.name


ram