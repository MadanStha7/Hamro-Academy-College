from django.db import models

from academics.models import Faculty, Grade
from common.constant import DISCOUNT_FINE_OPTIONS
from common.models import CommonInfo


class FeeSetup(CommonInfo):
    """
    model to store the fee type
    """

    name = models.CharField(max_length=64)
    faculty = models.ManyToManyField(Faculty, related_name="fee_setup")
    grade = models.ManyToManyField(Grade, related_name="fee_setup")
    due_date = models.DateField()

    def __str__(self):
        return "{} -- {}".format(self.name, self.institution)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(FeeSetup, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_on"]
        db_table = "fee_setup"


class DiscountType(CommonInfo):
    """
    Discount method information
    """

    name = models.CharField(max_length=50)
    discount_mode = models.CharField(
        max_length=1,
        choices=DISCOUNT_FINE_OPTIONS,
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return "{} -- {}".format(self.name, self.institution)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(DiscountType, self).save(*args, **kwargs)

    class Meta:
        db_table = "discount_type"
        verbose_name = "Discount Type"
        verbose_name_plural = "Discount Types"


class FineType(CommonInfo):
    """
    Fine method information
    """

    name = models.CharField(max_length=50)
    fine_mode = models.CharField(
        max_length=1,
        choices=DISCOUNT_FINE_OPTIONS,
    )
    fine_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return "{} -- {}".format(self.name, self.institution)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(FineType, self).save(*args, **kwargs)

    class Meta:
        db_table = "fine_type"
        verbose_name = "Fine Type"
        verbose_name_plural = "Fine Types"
