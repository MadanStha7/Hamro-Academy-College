import typing
from django.db.models import F
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from fees.domain.models import fee_setup_factory
from uuid import UUID
from fees.service_layer.serializers.fee_setup import FeeConfigSerializer
from student.models import StudentAcademicDetail
from fees.orm.models import (
    DiscountType,
    FeeCollection,
    FeeConfig,
    FeeSetup,
    StudentPaidFeeSetup,
    FineType,
)
from academics.models import SubjectGroup, Grade, Faculty


def get_fee_config(institution: UUID, grade=None, faculty=None):
    fee_setup_data = FeeSetup.objects.filter(institution=institution).values(
        "id", "name"
    )
    fee_config_data = FeeConfig.objects.filter(institution=institution).values(
        "id", "fee_type__id", "subject_group__id", "amount", "is_active"
    )
    subject_group_data = SubjectGroup.objects.filter(institution=institution).values(
        "id", "name"
    )
    if grade:
        fee_setup_data = fee_setup_data.filter(grade=grade)
        fee_config_data = fee_config_data.filter(subject_group__grade=grade)
        subject_group_data = subject_group_data.filter(grade=grade)
    if faculty:
        fee_setup_data = fee_setup_data.filter(faculty=faculty)
        fee_config_data = fee_config_data.filter(subject_group__faculty=faculty)
        subject_group_data = subject_group_data.filter(faculty=faculty)
    response_data = []
    for data in fee_setup_data:
        data_ = {
            "fee_type_id": data.get("id"),
            "fee_type_name": data.get("name"),
        }
        subject_group = []
        for subject in subject_group_data:
            subject_data = {
                "subject_group_id": subject.get("id"),
                "subject_group_name": subject.get("name"),
                "amount": 0,
                "fee_config_id": "",
                "is_active": False,
            }
            subject_group.append(subject_data)
        data_.update({"subject_group": subject_group})
        response_data.append(data_)

    for data in response_data:
        if data.get("subject_group"):
            for subject_group in data.get("subject_group"):
                for config_data in fee_config_data:
                    if config_data.get("fee_type__id") == data.get(
                        "fee_type_id"
                    ) and config_data.get("subject_group__id") == subject_group.get(
                        "subject_group_id"
                    ):
                        subject_group["amount"] = config_data.get("amount")
                        subject_group.update(
                            {
                                "fee_config_id": config_data.get("id"),
                                "is_active": config_data.get("is_active"),
                            }
                        )
    return response_data


def get_student_fee_collection(student_academic: UUID, institution: UUID):
    student_academic = get_object_or_404(StudentAcademicDetail, id=student_academic)
    fee_configs = (
        FeeConfig.objects.filter(
            subject_group__grade=student_academic.grade,
            subject_group__faculty=student_academic.faculty,
            institution=institution,
            is_active=True,
        ).select_related("fee_type", "subject_group")
    ).annotate(fee_type_name=F("fee_type__name"))

    serializer = FeeConfigSerializer(fee_configs, many=True)
    paid_fee_type = (
        StudentPaidFeeSetup.objects.filter(
            fee_collection__student_academic=student_academic
        )
        .order_by("fee_config__id")
        .values("fee_config__id", "due_amount")
    )
    for data in serializer.data:
        for paid_fee in paid_fee_type:
            if str(paid_fee.get("fee_config__id")) == data.get("id"):
                data["amount"] = str(paid_fee.get("due_amount"))
    data = [data for data in serializer.data if float(data.get("amount")) > 0]
    return data


def get_student_fee_collection_detail(
    student_academic: UUID,
    institution: UUID,
    fee_configs: typing.List[typing.Dict],
):
    """
    views to return the data, that is needed for student
    fee collection this includes, previous_collected_fees, applicable_fines
    """
    collected_student_fees = (
        StudentPaidFeeSetup.objects.filter(
            fee_collection__student_academic__id=student_academic,
            institution=institution,
        )
        .order_by("-created_on")
        .values("fee_config__id", "paid_amount", "due_amount")
    )

    fee_config_ids = [fee_config.get("fee_config") for fee_config in fee_configs]
    collected_fee_configs = FeeConfig.objects.filter(
        institution=institution, id__in=fee_config_ids, is_active=True
    ).values("id", "amount")
    applied_fines = []
    discounts = []
    for fee_config in fee_configs:
        applied_fines += fee_config.get("fines") if fee_config.get("fines") else []
        discounts += fee_config.get("discounts") if fee_config.get("discounts") else []

    applied_fines = FineType.objects.filter(
        institution=institution, id__in=applied_fines
    ).values("id", "fine_mode", "fine_amount")
    applied_discounts = DiscountType.objects.filter(
        institution=institution, id__in=discounts
    ).values("id", "discount_mode", "discount_amount")
    return (
        collected_student_fees,
        applied_fines,
        applied_discounts,
        collected_fee_configs,
    )


def get_student_collected_fee_invoices(student_academic: UUID, institution: UUID):
    """views to get the student invoice record information"""
    fee_collections = FeeCollection.objects.filter(
        student_academic=student_academic, institution=institution
    ).prefetch_related("student_paid_fee_setup")
    return fee_collections
