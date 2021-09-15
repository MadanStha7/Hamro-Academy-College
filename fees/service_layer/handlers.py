from fees.service_layer.serializers.fee_setup import FeeConfigSerializer
from django.db import transaction
from django.contrib.auth import get_user_model
from uuid import UUID
import typing
from fees.domain import commands
from fees.domain import models
from fees.adapters.repository import FeeSetupRepository, FeeConfigRepository
from academics.adapters.repository import SubjectGroupRepository
from fees.service_layer import views

User = get_user_model()


def get_fee_setup(institution: UUID, pk=None):
    repository = FeeSetupRepository()
    data = repository.get(institution=institution, pk=pk)
    return data


def add_fee_setup(institution: UUID, created_by: User, cmd: commands.AddFeeSetup):
    repository = FeeSetupRepository()
    fee_setup = models.fee_setup_factory(**cmd.__dict__)
    with transaction.atomic():
        fee_setup = repository.add(fee_setup, created_by, institution)
    return fee_setup


def add_fee_config(
    instiution: UUID, created_by: User, cmds: typing.List[commands.AddFeeConfig]
) -> None:
    repository = FeeConfigRepository()
    fee_configs = []
    existing_fee_configs = repository.get(institution=instiution).values(
        "id", "subject_group__id", "fee_type__id"
    )
    for cmd in cmds:
        fee_config = models.fee_config_factory(
            **cmd.__dict__, existing_fee_configs=existing_fee_configs
        )
        fee_configs.append(fee_config)
    with transaction.atomic():
        fee_config = repository.add(fee_configs, created_by, instiution)


def activate_deactivate_fee_config(cmd: commands.ActivateDeactivateFeeConfig):
    repository = FeeConfigRepository()
    fee_config = models.activate_deactivate_fee_config_factory(**cmd.__dict__)
    with transaction.atomic():
        fee_config = repository.activate_deactivate_fee_config(fee_config)
    return fee_config


def collect_student_fee(
    cmd: commands.CollectStudentFee, student_academic, institution, created_by
):
    (
        collected_student_fees,
        applied_fines,
        applied_discounts,
        collected_fee_configs,
    ) = views.get_student_fee_collection_detail(
        student_academic, institution, cmd.fee_configs
    )
    repository = FeeConfigRepository()
    model = models.student_fee_collect_factory(
        student_academic,
        cmd,
        collected_student_fees,
        applied_fines,
        applied_discounts,
        collected_fee_configs,
    )
    print(model)
    with transaction.atomic():
        repository.collect_student_fee_config(model, institution, created_by)
