from common.constant import CONTRACT_TYPE
from dataclasses import dataclass
import typing
from uuid import UUID
import datetime
import decimal


class Command:
    pass


@dataclass
class AddFeeSetup(Command):
    name: str
    faculty_id: typing.List[UUID]
    grade_id: typing.List[UUID]
    fee_type: str
    due_date: typing.Optional[datetime.date] = None
    due_day: typing.Optional[int] = None
    due_type: typing.Optional[int] = None
    description: typing.Optional[str] = None


@dataclass
class AddFeeConfig(Command):
    subject_group: UUID
    fee_type: UUID
    amount: decimal.Decimal
    id_: typing.Optional[UUID] = None


@dataclass
class ActivateDeactivateFeeConfig(Command):
    fee_config: UUID


@dataclass
class StudentFeeSetupCollect(Command):
    fee_config: UUID
    paid_amount: decimal.Decimal


@dataclass
class CollectStudentFee(Command):
    fee_configs: typing.List[StudentFeeSetupCollect]
    payment_method: str
    fine_id: typing.Optional[UUID] = None
    discount_in: typing.Optional[str] = None
    discount: typing.Optional[decimal.Decimal] = None
    narration: typing.Optional[str] = None


@dataclass
class AddScholarship(Command):
    name: str
    scholarship_in: str
    scholarship: decimal.Decimal
    fee_config: typing.List[UUID]
