from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from rest_framework import status
from rest_framework.response import Response

from common.administrator.viewset import CommonInfoViewSet
from student.administator.serializer.student import (
    StudentInfoSerializer,
    StudentListInfoSerializer,
)
from student.models import StudentInfo

User = get_user_model()


class StudentInfoViewSet(CommonInfoViewSet):
    """
    CRUD for student information or student details.
    """

    queryset = StudentInfo.objects.none()
    serializer_class = StudentInfoSerializer
    filter_fields = ["student_category"]
    search_fields = ["student_user__first_name", "student_user__last_name"]

    def get_queryset(self):
        queryset = StudentInfo.objects.filter(
            institution=self.request.institution
        ).annotate(category_name=F("student_category__name"))
        return queryset

    def list(self, request, *args, **kwargs):
        """api to get list of serialzer of student"""
        queryset = StudentInfo.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            phone=F("user__phone"),
            student_first_name=F("user__first_name"),
            student_last_name=F("user__last_name"),
            guardian_first_name=F("guardian_detail__user__first_name"),
            guardian_last_name=F("guardian_detail__user__last_name"),
            guardian_phone_number=F("guardian_detail__phone"),

        )
        serializer = StudentListInfoSerializer(queryset, many=True)
        return Response(serializer.data)

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
            Delete guardian based on the db ACID transition
            """
        instance = self.get_object()
        obj = self.get_object().id
        if instance.student:
            instance.student.delete()
        instance.user.delete()
        self.perform_destroy(instance)
        return Response(
            {"message": f"object {obj} successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
