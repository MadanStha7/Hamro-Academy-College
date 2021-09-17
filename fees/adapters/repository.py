import typing
from rest_framework.generics import get_object_or_404
from uuid import UUID
from fees.orm import models as orm
from core import models as core_orm
from user import models as user_orm
from academics import models as academic_orm
from fees.domain import models


class FeeSetupRepository:
    def __init__(self) -> None:
        pass

    def get(self, institution: UUID, pk=None) -> orm.FeeSetup:
        if pk:
            fee_setup = get_object_or_404(orm.FeeSetup, id=pk)
            return fee_setup
        fee_setups = orm.FeeSetup.objects.filter(institution=institution)
        return fee_setups

    def add(
        self,
        model: models.FeeSetup,
        created_by: user_orm.SystemUser,
        institution: UUID,
    ):
        values = {
            "name": model.name,
            "faculty": model.faculty,
            "grade": model.grade,
            "due_date": model.due_date,
            "fee_type": model.fee_type,
            "due_day": model.due_day,
            "due_type": model.due_type,
            "created_by": created_by,
            "institution": institution,
        }
        facultys = values.pop("faculty")
        grades = values.pop("grade")
        fee_setup = orm.FeeSetup.objects.create(**values)
        for faculty in facultys:
            fee_setup.faculty.add(faculty)
        for grade in grades:
            fee_setup.grade.add(grade)
        fee_setup.save()
        return fee_setup


class FeeConfigRepository:
    def __init__(self) -> None:
        pass

    def get(self, institution: UUID) -> orm.FeeConfig:
        data = orm.FeeConfig.objects.filter(institution=institution)
        return data

    def add(
        self,
        fee_configs: models.FeeConfig,
        created_by: user_orm.SystemUser,
        institution: UUID,
    ) -> None:
        fee_config_object_list_new = []
        fee_config_object_list_update = []
        for config in fee_configs:
            if config.id_:
                fee_config = orm.FeeConfig(id=config.id_)
                fee_config.amount = config.amount
                fee_config.modified_by = created_by
                fee_config_object_list_update.append(fee_config)
            else:
                fee_config = orm.FeeConfig(
                    subject_group=academic_orm.SubjectGroup(id=config.subject_group),
                    fee_type=orm.FeeSetup(id=config.fee_type),
                    amount=config.amount,
                    created_by=created_by,
                    institution=institution,
                )
                fee_config_object_list_new.append(fee_config)

        orm.FeeConfig.objects.bulk_create(fee_config_object_list_new)
        orm.FeeConfig.objects.bulk_update(
            fee_config_object_list_update, fields=["amount"]
        )

    def activate_deactivate_fee_config(
        self, fee_config: models.ActivateDeactivateFeeConfig
    ) -> None:
        fee_config_ = get_object_or_404(orm.FeeConfig, id=fee_config.fee_config)
        fee_config_.is_active = not fee_config_.is_active
        fee_config_.save()
        return fee_config_

    def collect_student_fee_config(
        self, student_academic: UUID, cmd, total_fee_amount_to_pay, total_paid_amount
    ):
        pass


class ScholarshipRepository:
    def __init__(self) -> None:
        pass

    def get(self, institution: UUID) -> orm.Scholarship:
        data = orm.Scholarship.objects.filter(institution=institution)
        return data

    def add(
            self,
            model: models.Scholarship,
            created_by: user_orm.SystemUser,
            institution: UUID,
    ):
        values = {
            "name": model.name,
            "scholarship_in": model.scholarship_in,
            "scholarship": model.scholarship,
            "fee_config": model.fee_config,
            "created_by": created_by,
            "institution": institution,
        }
        fee_config = values.pop("fee_config")
        scholarship = orm.Scholarship.objects.create(**values)
        for fee_config in fee_config:
            scholarship.fee_config.add(fee_config)
        scholarship.save()
        return scholarship
