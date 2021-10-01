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
    due_type: typing.Optional[str] = None
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
    fines: typing.Optional[typing.List[UUID]]
    discounts: typing.Optional[typing.List[UUID]]


@dataclass
class CollectStudentFee(Command):
    fee_configs: typing.List[StudentFeeSetupCollect]
    receipt_no: str
    payment_method: str
    narration: typing.Optional[str] = None
<<<<<<< HEAD


@dataclass
class AddScholarship(Command):
    name: str
    scholarship_in: str
    scholarship: decimal.Decimal
    fee_config: typing.List[UUID]
=======
    issued_date: typing.Optional[datetime.date] = datetime.date.today()


@dataclass
class UpdateStudentPaidFeeConfig(Command):
    paid_fee_config: UUID
    paid_amount: decimal.Decimal
>>>>>>> 99d178ed1e1151a148757ae8435c9fce70bedea4
