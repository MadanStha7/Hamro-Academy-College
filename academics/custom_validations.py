from rest_framework import serializers

from academics.helpers import teacher_grade_section_subject_shift


def validate_teacher_grade(value, user) -> None:
    """
    helper function to validate if teacher is assigned on particular grade or not
    """
    grades, sections, subjects, shifts = teacher_grade_section_subject_shift(user)
    if str(value.id) not in grades:
        raise serializers.ValidationError("unauthorized grade access")


def validate_teacher_section(value, user) -> None:
    """
    helper function to validate if teacher is assigned on particular section or not
    """
    grades, sections, subjects, shifts = teacher_grade_section_subject_shift(user)
    if str(value.id) not in sections:
        raise serializers.ValidationError("unauthorized section access")


def validate_teacher_subject(value, user) -> None:
    """
    helper function to validate if teacher is assigned on particular subject or not
    """
    grades, sections, subjects, shifts = teacher_grade_section_subject_shift(user)
    if str(value.id) not in subjects:
        raise serializers.ValidationError("unauthorized subject access")




