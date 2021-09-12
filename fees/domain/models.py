from pydantic import BaseModel
import typing
from uuid import UUID
import datetime
import decimal
from fees.domain import commands, exceptions


class FeeSetup(BaseModel):
    name: str
    faculty: typing.List[UUID]
    grade: typing.List[UUID]
    due_date: typing.Optional[datetime.date]
    fee_type: str
    due_day: typing.Optional[int]
    due_type: typing.Optional[int]
    description: typing.Optional[str]


class FeeConfig(BaseModel):
    id_: typing.Optional[UUID]
    subject_group: UUID
    fee_type: UUID
    amount: decimal.Decimal


class ActivateDeactivateFeeConfig(BaseModel):
    fee_config: UUID


class FeeCollect(BaseModel):
    student_academic: UUID
    fee_configs: typing.List[typing.Dict]
    total_amount_to_pay: decimal.Decimal
    total_paid_amount: decimal.Decimal
    payment_method: str
    fine_id: typing.Optional[UUID] = None
    discount_in: typing.Optional[str] = None
    discount: typing.Optional[decimal.Decimal] = None
    narration: typing.Optional[str] = None


def fee_setup_factory(
    name: str,
    faculty_id: typing.List[UUID],
    grade_id: typing.List[UUID],
    due_date: typing.Optional[datetime.date],
    fee_type: str,
    due_day: typing.Optional[int],
    due_type: typing.Optional[int],
    description: typing.Optional[str],
) -> FeeSetup:

    return FeeSetup(
        name=name,
        faculty=faculty_id,
        grade=grade_id,
        due_date=due_date,
        fee_type=fee_type,
        due_day=due_day,
        due_type=due_type,
        description=description,
    )


def fee_config_factory(
    id_: typing.Optional[UUID],
    subject_group: UUID,
    fee_type: UUID,
    amount: decimal.Decimal,
    existing_fee_configs: typing.List[typing.Dict],
) -> FeeConfig:
    for fee_config in existing_fee_configs:
        if (
            str(fee_config.get("subject_group__id")) == subject_group
            and str(fee_config.get("fee_type__id")) == fee_type
        ):
            return FeeConfig(
                id_=fee_config.get("id"),
                subject_group=fee_config.get("subject_group__id"),
                fee_type=fee_config.get("fee_type__id"),
                amount=amount,
            )
    return FeeConfig(
        id_=id_,
        subject_group=subject_group,
        fee_type=fee_type,
        amount=amount,
    )


def activate_deactivate_fee_config_factory(
    fee_config: UUID,
) -> ActivateDeactivateFeeConfig:
    return ActivateDeactivateFeeConfig(fee_config=fee_config)


def student_fee_collect_factory(
    student_academic: UUID,
    cmd: commands.CollectStudentFee,
    collected_student_fees: typing.List[typing.Dict],
    applicable_fines: typing.Optional[typing.List[typing.Dict]],
    collected_fee_configs: typing.List[typing.Dict],
) -> FeeCollect:
    total_paid_amount = 0
    for fee_type in cmd.fee_configs:
        total_paid_amount += fee_type.get("paid_amount")

    # checking if user is paying more amount than the amount
    # he has to pay and checking if particular fee_config is paid or not
    for fee in collected_student_fees:
        for fee_config in cmd.fee_configs:
            if str(fee.get("fee_type__id")) == fee_config.get("fee_type"):
                if fee_config.get("paid_amount") > fee.get("due_amount"):
                    raise exceptions.PaidAmountExceedException(
                        "Paid amount on particular fee type exceed more than to be paid"
                    )
                if fee.get("due_amount") == 0:
                    raise exceptions.DuplicateFeeConfigPaidException(
                        f"fee_config {fee_config.get('fee_config')} is already paid and no due remaining"
                    )

    total_fee_amount_to_pay = 0
    # calculating the due_amount and checking if user is paying more amount the the amount he has to pay
    for collected_fee_config in collected_fee_configs:
        for fee_config in cmd.fee_configs:
            if str(collected_fee_config.get("id")) == fee_config.get("fee_config"):
                if collected_fee_config.get("amount") < fee_config.get("paid_amount"):
                    raise exceptions.PaidAmountExceedException(
                        "Paid amount on particular fee type exceed more than to be paid"
                    )
                elif collected_fee_config.get("amount") > fee_config.get("paid_amount"):
                    fee_config.update(
                        {
                            "due_amount": collected_fee_config.get("amount")
                            - fee_config.get("paid_amount")
                        }
                    )

                total_fee_amount_to_pay += collected_fee_config.get("amount")

    # adding the fines to the fee
    for fine in cmd.fine_id:
        if applicable_fines:
            for applicable_fine in applicable_fines:
                if str(applicable_fine.get("id")) == fine:
                    total_fee_amount_to_pay += (
                        applicable_fine.get("fee_amount")
                        if applicable_fine.get("mode") == "A"
                        else (
                            total_fee_amount_to_pay
                            * applicable_fine.get("fee_amount")
                            / 100
                        )
                    )

    total_fee_amount_to_pay -= (
        cmd.discount
        if cmd.discount_id == "A"
        else (total_fee_amount_to_pay * cmd.discount / 100)
    )

    return FeeCollect(
        student_academic=student_academic,
        fee_configs=cmd.fee_configs,
        total_amount_to_pay=total_fee_amount_to_pay,
        total_paid_amount=total_paid_amount,
        payment_method=cmd.payment_method,
        fine_id=cmd.fine_id,
        discount_in=cmd.discount_in,
        discount=cmd.discount,
        narration=cmd.narration,
    )
