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


def get_student_list_online_attendance(online_class_info, general_info):
    """
    helper function to get the list of student of particular class and section
    to know, whether student have joined online class or not
    """
    student_academics = (
        StudentAcademicDetail.objects.filter(
            grade=online_class_info.grade,
            section=online_class_info.section,
            academic_session__status=True,
            general_info=general_info,
        )
        .exclude(~Q(student_online_class_attendance=None))
        .annotate(
            student_academic=F("id"),
            grade_name=F("grade__name"),
            section_name=F("section__name"),
            student_first_name=F("student__user__first_name"),
            student_last_name=F("student__user__last_name"),
        )
        .values(
            "id",
            "student_academic",
            "grade_name",
            "section_name",
            "student_first_name",
            "student_last_name",
        )
    )
    for student in student_academics:
        student.update({"joined_on": None})
    return student_academics
