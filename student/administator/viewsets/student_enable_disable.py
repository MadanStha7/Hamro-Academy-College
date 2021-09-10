from django.db.models import F
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from student.administator.serializer.student_enable_disable import (
    StudentListInfoSerializer,
)
from permissions.administrator import AdministratorPermission
from student.models import StudentInfo
from student.administator.custom_fiter import StudentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response


class StudentDisableAPIView(APIView):
    """Api to display a disable Student list in adminstrator"""

    serializer_class = StudentListInfoSerializer
    queryset = StudentInfo.objects.none()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "guardian_detail__user__first_name",
        "guardian_detail__user__last_name",
    ]
    filter_class = StudentFilter
    permission_classes = (IsAuthenticated, AdministratorPermission)

    def get(self, request, format=None):
        queryset = StudentInfo.objects.filter(
            disable=True, institution=self.request.institution
        )
        queryset = queryset.annotate(
            phone=F("user__phone"),
            student_first_name=F("user__first_name"),
            student_middle_name=F("user__middle_name"),
            student_last_name=F("user__last_name"),
            student_email=F("user__email"),
            student_phone=F("user__phone"),
            faculty=F("student_academic_detail__faculty__name"),
            section=F("student_academic_detail__section__name"),
            grade=F("student_academic_detail__grade__name"),
            guardian_first_name=F("guardian_detail__user__first_name"),
            guardian_last_name=F("guardian_detail__user__last_name"),
            relation_name=F("guardian_detail__relation"),
            email=F("user__email"),
        )
        serializer = StudentListInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        with transaction.atomic():
            student = self.request.data.get("student", False)
            # check if same student id exist or not
            if len(student) > 0:
                student_list = []
                for id_ in student:
                    if student.count(id_) > 1:
                        raise ValidationError(
                            {"error": ["Same student cannot be disabled"]}
                        )
                    status = self.request.query_params.get("status", None)
                    student_obj = get_object_or_404(
                        StudentInfo,
                        id=id_,
                        institution=self.request.institution,
                    )
                    # enable student
                    if status == "enable":
                        if student_obj.disable == True:
                            student_obj.disable = False
                            student_list.append(student_obj)
                        else:
                            raise ValidationError(
                                {
                                    "error": [
                                        "Please provide the enable students id in list"
                                    ]
                                }
                            )
                    # disable  student
                    elif status == "disable":
                        if student_obj.disable == False:
                            student_obj.disable = True
                            student_list.append(student_obj)
                        else:
                            raise ValidationError(
                                {
                                    "error": [
                                        "Please provide the disable students id in list"
                                    ]
                                }
                            )
                    else:
                        raise ValidationError(
                            {"error": ["Provide status in query params"]}
                        )
                StudentInfo.objects.bulk_update(student_list, ["disable"])
                return Response({"success": ["Students successfully updated"]})

            else:
                raise ValidationError({"error": ["Student id is required"]})


class StudentDisableDeleteAPIView(APIView):
    """delete the student disable list"""

    def post(self, request, format=None):
        student = self.request.data.get("student", False)
        if student:

            student_obj = [
                student_id for student_id in student if student.count(student_id) > 1
            ]
            if student_obj:
                raise ValidationError({"error": ["Same student cannot be disabled"]})
            for student_id in student:
                student_obj = get_object_or_404(
                    StudentInfo,
                    id=student_id,
                    institution=self.request.institution,
                )
                student_obj.delete()
                return Response({"message": "Student successfully deleted"})
