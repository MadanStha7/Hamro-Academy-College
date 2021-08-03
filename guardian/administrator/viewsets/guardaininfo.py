from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from common.administrator.viewset import CommonInfoViewSet
from guardian.administrator.serializer.guardianinfo import (
    GuardianInfoSerializer,
    StudentGuardianInfoSerializer,
)

from student.models import StudentGuardianInfo, StudentInfo

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

    def perform_create(self, serializer):
        """
        Create guardian based on image of the guardian.
        """
        photo = self.request.data.get("photo")
        if self.request.institution:
            serializer.save(
                photo=photo,
                institution=self.request.institution,
                created_by=self.request.user,
            )

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


class StudentGuardianInfoView(CreateAPIView):
    queryset = StudentGuardianInfo.objects.none()
    serializer_class = GuardianInfoSerializer

    def perform_create(self, serializer):
        photo = self.request.data.get("photo")
        if self.request.institution:
            serializer.save(
                photo=photo,
                created_by=self.request.user,
                institution=self.request.institution,
            )
        else:
            return Response(
                {"message": "You must be a institute student to perform this action"}
            )

    def create(self, request, *args, **kwargs):
        new = self.request.query_params.get("new")
        student = self.request.query_params.get("student")
        if student:
            guardian = self.request.data.get("guardian")

            if new == "false":

                student = StudentInfo.objects.get(id=student)
                student.guardian_detail = guardian
                student.save()

            elif new == "true":
                serializer = GuardianInfoSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                guardian = serializer.save()
                student = StudentInfo.objects.get(id=student)
                student.guardian_detail = guardian
                student.save()
            return Response({"message": "Guardain with this student already exist."})
