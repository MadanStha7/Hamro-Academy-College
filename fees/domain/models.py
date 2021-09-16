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
    due_type: typing.Optional[str]
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
    receipt_no: str
    fee_configs: typing.List[typing.Dict]
    total_amount_to_pay: decimal.Decimal
    total_paid_amount: decimal.Decimal
    payment_method: str
    narration: typing.Optional[str] = None
    issued_date: typing.Optional[datetime.date] = datetime.date.today()


def fee_setup_factory(
    name: str,
    faculty_id: typing.List[UUID],
    grade_id: typing.List[UUID],
    due_date: typing.Optional[datetime.date],
    fee_type: str,
    due_day: typing.Optional[int],
    due_type: typing.Optional[str],
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
    applicable_discounts: typing.Optional[typing.List[typing.Dict]],
    collected_fee_configs: typing.List[typing.Dict],
) -> FeeCollect:
    total_paid_amount = 0
    paying_fee_configs = []

    for fee_config in cmd.fee_configs:
        total_paid_amount += fee_config.get("paid_amount")
        paying_fee_configs.append(fee_config.get("fee_config"))

    if len(paying_fee_configs) != len(set(paying_fee_configs)):
        raise exceptions.SameFeeConfigMultipleTimeException(
            "You are not allowed to pay two fee configs separately"
        )

    [
        fee_config.update({"amount_to_pay": collected_fee_config.get("amount")})
        for fee_config in cmd.fee_configs
        for collected_fee_config in collected_fee_configs
        if fee_config.get("fee_config") == str(collected_fee_config.get("id"))
    ]

    for fee_config in cmd.fee_configs:
        if fee_config.get("fines"):
            amount_to_pay = fee_config.get("amount_to_pay")
            for fine in applicable_fines:
                if str(fine.get("id")) in fee_config.get("fines"):
                    fee_config["amount_to_pay"] += (
                        fine.get("fine_amount")
                        if fine.get("fine_mode") == "A"
                        else (amount_to_pay * fine.get("fine_amount") / 100)
                    )

        if fee_config.get("discounts"):
            amount_to_pay = fee_config.get("amount_to_pay")
            for discount in applicable_discounts:
                if str(discount.get("id")) in fee_config.get("discounts"):
                    fee_config["amount_to_pay"] -= (
                        discount.get("discount_amount")
                        if discount.get("discount_mode") == "A"
                        else (amount_to_pay * discount.get("discount_amount") / 100)
                    )

    # checking if user is paying more amount than the amount
    # he has to pay and checking if particular fee_config is paid or not
    for fee in collected_student_fees:
        for fee_config in cmd.fee_configs:
            if str(fee.get("fee_config__id")) == fee_config.get("fee_config"):
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
    for fee_config in cmd.fee_configs:
        if fee_config.get("amount_to_pay") < fee_config.get("paid_amount"):
            raise exceptions.PaidAmountExceedException(
                "Paid amount on particular fee type exceed more than to be paid"
            )
        elif fee_config.get("amount_to_pay") >= fee_config.get("paid_amount"):
            if collected_student_fees:
                for student_paid in collected_student_fees:
                    if str(student_paid.get("fee_config__id")) == fee_config.get(
                        "fee_config"
                    ):
                        if student_paid.get("due_amount") > 0:
                            if student_paid.get("due_amount") > fee_config.get(
                                "paid_amount"
                            ):
                                fee_config.update(
                                    {
                                        "due_amount": student_paid.get("due_amount")
                                        - fee_config.get("paid_amount")
                                    }
                                )
                                break
                            elif student_paid.get("due_amount") < fee_config.get(
                                "paid_amount"
                            ):
                                raise exceptions.PaidAmountExceedException(
                                    "Paid amount on particular fee type exceed more than to be paid"
                                )
                            else:
                                fee_config.update({"due_amount": 0})
                                break
                    else:
                        fee_config.update(
                            {
                                "due_amount": fee_config.get("amount_to_pay")
                                - fee_config.get("paid_amount")
                            }
                        )

            else:
                fee_config.update(
                    {
                        "due_amount": fee_config.get("amount_to_pay")
                        - fee_config.get("paid_amount")
                    }
                )

            total_fee_amount_to_pay += fee_config.get("amount_to_pay")

    # adding the fines to the fee
    # for fine in cmd.fine_id:
    #     if applicable_fines:
    #         for applicable_fine in applicable_fines:
    #             if applicable_fine.get("id") == fine:
    #                 total_fee_amount_to_pay += (
    #                     applicable_fine.get("fee_amount")
    #                     if applicable_fine.get("mode") == "A"
    #                     else (
    #                         total_fee_amount_to_pay
    #                         * applicable_fine.get("fee_amount")
    #                         / 100
    #                     )
    #                 )

    # if cmd.discount:
    #     total_fee_amount_to_pay -= (
    #         cmd.discount
    #         if cmd.discount_in == "A"
    #         else (total_fee_amount_to_pay * cmd.discount / 100)
    #     )

    return FeeCollect(
        student_academic=student_academic,
        fee_configs=cmd.fee_configs,
        total_amount_to_pay=total_fee_amount_to_pay,
        total_paid_amount=total_paid_amount,
        payment_method=cmd.payment_method,
        narration=cmd.narration,
        issued_date=cmd.issued_date,
        receipt_no=cmd.receipt_no,
    )
