from django.contrib.auth import get_user_model
from django.db.models import F, Q
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
        ).annotate(category_name=F("category__name"))
        return queryset

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
                general_info=self.request.general_info
            )
            return queryset

        def list(self, request, *args, **kwargs):
            """
            Retrieve all student info
            """
            institution = self.request.institution
            if self.request.query_params.get("disable") == "true":
                queryset = self.filter_queryset(self.get_queryset()).filter(
                    disable=True,
                    institution=institution,
                )
            else:
                queryset = self.filter_queryset(
                    self.get_queryset().filter(disable=False, institution=institution)
                )
            grade = self.request.query_params.get("grade")
            section = self.request.query_params.get("section")
            academic_session = self.request.query_params.get("academic_session")
            search = self.request.query_params.get("search")
            if search:
                queryset = queryset.filter(
                    Q(student_user__first_name__icontains=search)
                    | Q(student_user__last_name__icontains=search)
                )

            if academic_session:
                queryset = queryset.filter(
                    academic_info__academic_session__id=academic_session
                )
            else:
                queryset = queryset.filter(academic_info__academic_session__status=True)

            if grade:
                queryset = queryset.filter(academic_info__grade__id=grade)
                if section:
                    queryset = queryset.filter(academic_info__section__id=section)
            queryset = queryset.annotate(
                student_first_name=F("student_user__first_name"),
                student_last_name=F("student_user__last_name"),
                guardian_first_name=F("guardian_detail__guardian_user__first_name"),
                guardian_last_name=F("guardian_detail__guardian_user__last_name"),
                guardian_phone_number=F("guardian_detail__phone_number"),
                grade=F("academic_info__grade__name"),
                academic_id=F("academic_info__id"),
                section=F("academic_info__section__name"),
                roll_number=F("academic_info__roll_number"),
            )
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = StudentListInfoSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = StudentListInfoSerializer(queryset, many=True)
            return Response(serializer.data)

        def perform_create(self, serializer):
            guardian_detail = self.request.data.get("guardian_detail")
            if self.request.user.institution:
                serializer.save(
                    created_by=self.request.user,
                    institution=self.request.institution,
                    guardian_detail=StudentGuardianInfo.objects.get(id=guardian_detail),
                )
            else:
                raise

        def perform_update(self, serializer):
            student_photo_data = self.request.data.get("student_photo")
            student_document = self.request.data.get("student_document")
            if self.request.user.general_info:
                serializer.save(
                    student_photo=student_photo_data, student_document=student_document
                )
            else:
                return Response(
                    {"message": "You must be a school staff to perform this action"}
                )

        # def create(self, request, *args, **kwargs):
        #     get_active_session(self.request.general_info)
        #     return super(StudentInfoViewSet, self).create(request, *args, **kwargs)
