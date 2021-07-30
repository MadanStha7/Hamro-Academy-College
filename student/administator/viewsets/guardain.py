from common.administrator.viewset import CommonInfoViewSet
from student.administator.serializer.guardian import (
    GuardianInfoSerializer,
    GuardianListInfoSerializer,
)
from student.models import StudentGuardianInfo

from django.db import transaction
from django.db.models import F, Q
from rest_framework.response import Response
from rest_framework import status


class GuardianInfoViewSet(CommonInfoViewSet):
    queryset = StudentGuardianInfo.objects.none()
    serializer_class = GuardianInfoSerializer

    def get_queryset(self):
        """
        filtering guardian based on grade and section
        """
        queryset = StudentGuardianInfo.objects.filter(
            institution=self.request.institution
        )
        grade = self.request.query_params.get("grade")
        section = self.request.query_params.get("section")
        student = self.request.query_params.get("student")
        if grade:
            queryset = queryset.filter(
                student_guardian_detail__academic_info__grade__id=grade,
            )
        if section:
            queryset = queryset.filter(
                student_guardian_detail__academic_info__section__id=section,
            )
        if student:
            queryset = queryset.filter(student_guardian_detail__id=student)
        queryset = queryset.annotate(
            secondary_id=F("secondary_guardian__id"),
            secondary_full_name=F("secondary_guardian__full_name"),
            secondary_address=F("secondary_guardian__address"),
            secondary_phone=F("secondary_guardian__phone"),
        )

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Retrieve guardians list
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GuardianListInfoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = GuardianListInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        """
        Delete guardian based on the db ACID transition
        """
        instance = self.get_object()
        obj = self.get_object().id
        if instance.secondary_guardian:
            instance.secondary_guardian.delete()
        instance.user.delete()
        self.perform_destroy(instance)
        return Response(
            {"message": f"object {obj} successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
