from django.db.models import Q
from rest_framework import serializers

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
