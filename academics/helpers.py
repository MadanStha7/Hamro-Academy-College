import datetime

from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.db.models import BooleanField, Case, Q, When, F
from django.utils import timezone

from timetable.models import TimeTable


def teacher_grade_section_subject_shift(user):
    """
    helper function to get the grades, sections and subjects
    the teacher is teaching
    """
    academic_timetable = TimeTable.objects.filter(
        teacher=user, academic_session__status=True
    ).values("grade__id", "subject__id", "section__id", "shift__id")
    grades = [str(timetable.get("grade__id")) for timetable in academic_timetable]
    subjects = [str(timetable.get("subject__id")) for timetable in academic_timetable]
    sections = [str(timetable.get("section__id")) for timetable in academic_timetable]
    shifts = [str(timetable.get("shift__id")) for timetable in academic_timetable]
    if academic_timetable:
        return grades, sections, subjects, shifts
    raise ValidationError({"error": "unauthorized class access."})


def validate_date(value):
    """
    helper function to validate any date that should not accept past dates
    """
    if value < datetime.date.today():
        raise ValidationError("past date is not accepted")
    return value


def validate_start_end_time(value):
    if "start_time" in value and "end_time" in value:
        if value["start_time"] >= value["end_time"]:
            raise serializers.ValidationError(
                "start time should not be after and equal to end time"
            )


def get_online_class_values(queryset):
    time_now = timezone.now().strftime("%H:%M")
    queryset = queryset.annotate(
        subject_name=F("subject__name"),
        teacher_first_name=F("created_by__first_name"),
        teacher_last_name=F("created_by__last_name"),
        grade_name=F("grade__name"),
        section_name=F("section__name"),
        is_completed=Case(
            When(
                Q(class_date__lt=datetime.date.today()),
                # and Q(end_time__lt=time_now),
                then=True,
            ),
            When(
                Q(class_date=datetime.date.today()) and Q(end_time__lt=time_now),
                then=True,
            ),
            output_field=BooleanField(),
            default=False,
        ),
        is_upcoming=Case(
            When(
                Q(class_date__gte=datetime.date.today(), start_time__gt=time_now),
                then=True,
            ),
            output_field=BooleanField(),
            default=False,
        ),
        is_ongoing=Case(
            When(
                Q(class_date=datetime.date.today())
                and Q(start_time__lte=time_now, end_time__gte=time_now),
                then=True,
            ),
            output_field=BooleanField(),
            default=False,
        ),
    )
    return queryset


def online_class_helper(data, class_date, start_time, end_time):
    today_date = datetime.datetime.utcnow()
    today_date = today_date.strftime("%Y-%m-%d")

    time_now = timezone.now().strftime("%H:%M")
    if (class_date <= today_date) and (end_time < time_now):
        data.update({"is_completed": True})
    else:
        data.update({"is_completed": False})

    if (class_date == today_date) and (start_time > time_now):
        data.update({"is_upcoming": True})

    elif class_date > today_date:
        data.update({"is_upcoming": True})

    else:
        data.update({"is_upcoming": False})

    if class_date == today_date and (start_time < time_now) and (end_time > time_now):
        data.update({"is_ongoing": True})
    else:
        data.update({"is_ongoing": False})
    return data


