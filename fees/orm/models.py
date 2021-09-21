from django.db import models

from academics.models import Faculty, Grade, SubjectGroup
from common.constant import DISCOUNT_FINE_OPTIONS
from common.models import CommonInfo
from student.models import StudentAcademicDetail


class FeeSetup(CommonInfo):
    """
    model to store the fee type
    """

    FEE_TYPE = (("Monthly", "Monthly"), ("Yearly", "Yearly"))
    DUE_TYPE = (("Prior", "Prior"), ("After", "After"))
    name = models.CharField(max_length=64)
    faculty = models.ManyToManyField(Faculty, related_name="fee_setup")
    grade = models.ManyToManyField(Grade, related_name="fee_setup")
    due_date = models.DateField(blank=True, null=True)
    fee_type = models.CharField(choices=FEE_TYPE, max_length=31, blank=True, null=True)
    due_day = models.IntegerField(default=0, blank=True, null=True)
    due_type = models.CharField(choices=DUE_TYPE, max_length=7, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

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


class FeeConfig(CommonInfo):
    subject_group = models.ForeignKey(
        SubjectGroup,
        related_name="fee_config",
        on_delete=models.CASCADE,
        help_text="Fee applied to particular subject group",
    )
    fee_type = models.ForeignKey(
        FeeSetup, related_name="fee_config", on_delete=models.CASCADE
    )
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{self.fee_type.name} - {self.amount}"

    def save(self, *args, **kwargs):
        if self.amount < 0:
            self.amount = 0
        return super(FeeConfig, self).save(*args, **kwargs)

    class Meta:
        db_table = "fee_config"


class FeeCollection(CommonInfo):
    DISCOUNT_OPTIONS = (("P", "Percentage"), ("A", "Amount"))
    PAYMENT_METHOD = (("cash", "Cash"), ("bank-transfer", "Bank Transfer"))
    receipt_no = models.CharField(
        max_length=31, null=True, help_text="Receipt ID of the student fee payment"
    )
    student_academic = models.ForeignKey(
        StudentAcademicDetail, related_name="fee_collection", on_delete=models.CASCADE
    )
    issued_date = models.DateField(help_text="Date when student paid fee")
    total_amount_to_pay = models.DecimalField(
        max_digits=20, decimal_places=2, help_text="Amount student need to pay"
    )
    discount_in = models.CharField(
        choices=DISCOUNT_OPTIONS, max_length=1, blank=True, null=True
    )
    discount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Discount amount or percentage",
    )
    fine = models.ManyToManyField(FineType, related_name="fee_collection", blank=True)
    total_paid_amount = models.DecimalField(
        max_digits=20, decimal_places=2, help_text="Total amount student paid"
    )
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=31)
    narration = models.TextField(blank=True, null=True)

    @property
    def get_due_amount(self):
        return self.total_amount_to_pay - self.total_paid_amount

    class Meta:
        db_table = "fee_collection"
        ordering = ["-created_on"]


class StudentPaidFeeSetup(CommonInfo):
    """model for storing the student paid particular fee setup(type)"""

    fee_collection = models.ForeignKey(
        FeeCollection,
        related_name="student_paid_fee_setup",
        on_delete=models.CASCADE,
        help_text="Master fee collection",
    )
    fee_config = models.ForeignKey(
        FeeConfig,
        related_name="student_paid_fee_setup",
        on_delete=models.PROTECT,
        help_text="Type of fee config student paid",
        blank=True,
        null=True,
    )
    total_amount_to_pay = models.DecimalField(max_digits=20, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=2)
    due_amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.fee_config.fee_type.name}"

    class Meta:
        db_table = "student_paid_fee_setup"
        ordering = ["-created_on"]


class FeeAppliedFine(CommonInfo):
    """model to stores the fines that is applied in particular fee type"""

    student_paid_fee_setup = models.ForeignKey(
        StudentPaidFeeSetup, related_name="fee_applied_fine", on_delete=models.CASCADE
    )
    fine = models.ForeignKey(
        FineType, related_name="fee_applied_fine", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "fee_applied_fine"
        ordering = ["-created_on"]


class FeeAppliedDiscount(CommonInfo):
    """model to stores the discounts that is applied in particular fee type"""

    student_paid_fee_setup = models.ForeignKey(
        StudentPaidFeeSetup,
        related_name="fee_applied_discount",
        on_delete=models.CASCADE,
    )
    discount = models.ForeignKey(
        DiscountType, related_name="fee_applied_discount", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "fee_applied_discount"
        ordering = ["-created_on"]


class StudentPaidFeeSetupUpdateLog(CommonInfo):
    """model to save the log if user update the student fee logs"""

    paid_fee_setup = models.ForeignKey(
        StudentPaidFeeSetup,
        related_name="student_paid_fee_setup_update_log",
        on_delete=models.CASCADE,
    )
    previous_amount = models.DecimalField(max_digits=20, decimal_places=2)
    updated_amount = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = "student_paid_fee_setup_update_log"
        ordering = ["-created_on"]
