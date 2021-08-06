from django.contrib.auth import get_user_model
from django.db.models import F, Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from common.administrator.viewset import CommonInfoViewSet
from student.administator.serializer.student import (
    StudentInfoSerializer,
    StudentListInfoSerializer,
)
from student.models import StudentInfo, StudentGuardianInfo

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

    class StudentInfoViewSet(CommonInfoViewSet):
        """
        CRUD for student information or student details.
        """

        queryset = StudentInfo.objects.none()
        serializer_class = StudentInfoSerializer
        filter_fields = ["student_category"]
        search_fields = ["user__first_name", "user__last_name"]

        # def get_queryset(self):
        #     queryset = StudentInfo.objects.filter(
        #         general_info=self.request.general_info
        #     )
        #     return queryset

        def list(self, request, *args, **kwargs):
            """
            Retrieve all student info
            """
            institution = self.request.institution
            queryset = StudentInfo.objects.filter(institution=institution).annotate(
                student_first_name=F("user__first_name"),
                student_last_name=F("user__last_name"),
                guardian_first_name=F("guardian_detail__user__first_name"),
                guardian_last_name=F("guardian_detail__user__last_name"),
                guardian_phone_number=F("guardian_detail__phone_number"),
            )
            search = self.request.query_params.get("search")
            if search:
                queryset = queryset.filter(
                    Q(user__first_name__icontains=search)
                    | Q(user__last_name__icontains=search)
                )

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = StudentListInfoSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = StudentListInfoSerializer(queryset, many=True)
            return Response(serializer.data)

        def perform_create(self, serializer):
            # photo = self.request.data.get("photo")
            serializer.save(
                created_by=self.request.user,
                institution=self.request.institution,
            )

        #
        # def perform_create(self, serializer):
        #     photo = self.request.data.get("photo")
        #     if self.request.institution:
        #         serializer.save(
        #
        #         )
        #     else:
        #         raise ValidationError("you are not enroll in this institution")

        def disable_or_enable_student(self, request):
            student_id = self.request.query_params.get("student")
            if student_id:
                student = get_object_or_404(StudentInfo, id=student_id)
                if student:
                    if student.disable:
                        student.disable = False
                    else:
                        student.disable = True
                    student.save()

                    serializer = self.get_serializer(student)

                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(
                    {"error": " student not found"}, status=status.HTTP_404_NOT_FOUND
                )
            raise ValidationError("Guardian Info with this student id already exist")
