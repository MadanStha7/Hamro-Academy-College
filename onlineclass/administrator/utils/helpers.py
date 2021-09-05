from rest_framework.exceptions import ValidationError
import datetime


def validate_date(value):
    """
    helper function to validate any date that should not accept past dates
    """
    if value < datetime.date.today():
        raise ValidationError("Past date is not accepted")
    return value
