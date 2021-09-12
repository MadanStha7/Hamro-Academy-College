import typing
from django.db.models import F
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from fees.domain.models import fee_setup_factory
from uuid import UUID
from fees.service_layer.serializers.fee_setup import FeeConfigSerializer
from student.models import StudentAcademicDetail
from fees.orm.models import FeeConfig, FeeSetup, StudentPaidFeeSetup, FineType
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
    paid_fee_type = StudentPaidFeeSetup.objects.filter(
        fee_collection__student_academic=student_academic
    ).values("fee_type__id", "due_amount")
    for data in serializer.data:
        for paid_fee in paid_fee_type:
            if paid_fee.get("fee_type__id") == data.get("fee_type"):
                data["amount"] = paid_fee.get("due_amount")
    return serializer.data


def get_student_fee_collection_detail(
    student_academic: UUID,
    institution: UUID,
    fine_id: typing.List[UUID],
    fee_types: typing.List[typing.Dict],
):
    """
    views to return the data, that is needed for student
    fee collection this includes, previous_collected_fees, applicable_fines
    """
    collected_student_fees = StudentPaidFeeSetup.objects.filter(
        fee_collection__student_academic__id=student_academic, institution=institution
    ).values("fee_type__id", "paid_amount", "due_amount")
    applied_fines = FineType.objects.filter(
        institution=institution, id__in=fine_id
    ).values("id", "fine_mode", "fine_amount")
    collected_fee_configs = FeeConfig.objects.filter(
        institution=institution, id__in=fee_types, is_active=True
    ).values("id", "amount")
    return collected_student_fees, applied_fines, collected_fee_configs
