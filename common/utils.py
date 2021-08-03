import base64
import uuid

from django.core.files.base import ContentFile
from django.db.models import Q
from rest_framework import serializers
from academics.models import Grade
from common.constant import GRADE_CHOICES, SUBJECT_TYPES


def return_grade_name_of_value(name):
    for grade in GRADE_CHOICES:
        if grade[0] == name:
            return grade[1]
    return None


def get_subject_type_name_of_value(name):
    for subject_type in SUBJECT_TYPES:
        if subject_type[0] == name:
            return subject_type[1]
    return None


def validate_unique_name(model, value, institution, instance):
    if instance:
        if model.objects.filter(
            ~Q(id=instance.id), name=value.title(), institution=institution
        ).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this name already exists"
            )
    else:
        if model.objects.filter(name=value.title(), institution=institution).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this name already exists"
            )

    return value


def validate_unique_role(model, title, institution, instance):
    if instance:
        if model.objects.filter(
            ~Q(id=instance.id), title=title, institution=institution
        ).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this Group already exists."
            )
    else:
        if model.objects.filter(title=title, institution=institution).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this Group already exists."
            )

    return title


def validate_unique_faculty_grade(model, value, institution, instance):
    if instance:
        if model.objects.filter(
            ~Q(id=instance.id),
            faculty=value["faculty"],
            grade=value["grade"],
            institution=institution,
        ).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this faculty and grade already exists"
            )
    else:
        if model.objects.filter(
            faculty=value["faculty"], grade=value["grade"], institution=institution
        ).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this faculty and grade already exists"
            )

    return value
