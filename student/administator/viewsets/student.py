from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.administrator.viewset import CommonInfoViewSet
from permissions.administrator import AdministratorPermission
from permissions.administrator_or_front_desk import AdministratorOrFrontDeskOPermission
from permissions.front_desk_officer import FrontDeskPermission
from student.administator.custom_fiter import StudentFilter
from student.administator.serializer.student import (
    StudentInfoSerializer,
    StudentListInfoSerializer,
)
from student.models import StudentInfo
from rest_framework import filters

User = get_user_model()


class StudentInfoViewSet(CommonInfoViewSet):
    """
    CRUD for student information or student details.
    """

    queryset = StudentInfo.objects.none()
    serializer_class = StudentInfoSerializer
    permission_classes = (IsAuthenticated, AdministratorOrFrontDeskOPermission)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["user__first_name", "user__last_name", "guardian_detail__user__first_name",
                     "guardian_detail__user__last_name"]
    filter_class = StudentFilter

    def get_queryset(self):
        queryset = StudentInfo.objects.filter(
            institution=self.request.institution
        ).annotate(student_first_name=F("user__first_name"),
                   student_middle_name=F("user__middle_name"),
                   student_last_name=F("user__last_name"),)
        return queryset

    def list(self, request, *args, **kwargs):
        """api to get list of serializer of student"""
        institution = self.request.institution
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        page_ids = [i.id for i in page]
        result = queryset.filter(id__in=page_ids)
        result = result.annotate(
            phone=F("user__phone"),
            student_first_name=F("user__first_name"),
            student_middle_name=F("user__middle_name"),
            student_last_name=F("user__last_name"),
            faculty=F("student_academic_detail__faculty__name"),
            section=F("student_academic_detail__section__name"),
            grade=F("student_academic_detail__grade__name"),
            guardian_first_name=F("guardian_detail__user__first_name"),
            guardian_last_name=F("guardian_detail__user__last_name"),
            relation=F("guardian_detail__relation")
        )
        serializer = StudentListInfoSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        photo = self.request.data.get("photo")
        serializer.save(
            photo=photo,
            created_by=self.request.user,
            institution=self.request.institution,
        )

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        """
            Delete student
            """
        instance = self.get_object()
        obj = self.get_object().id
        instance.user.delete()
        self.perform_destroy(instance)
        return Response(
            {"message": f"object {obj} successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


