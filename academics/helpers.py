import datetime

from django.db.models import Q, F
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from student.models import StudentAcademicDetail
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

