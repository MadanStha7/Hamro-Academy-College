from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from student.frontdesk.serializer.student import StudentListInfoSerializer
from permissions.front_desk_officer import FrontDeskPermission
from student.models import StudentInfo
from student.administator.custom_fiter import StudentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.serializers import ValidationError


class StudentListAPIView(ListAPIView):
    """Api to display a Student list in front desk officer"""

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
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_queryset(self):
        queryset = StudentInfo.objects.filter(
            institution=self.request.institution, disable=False
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
        return queryset


class StudentRetrieveAPIView(RetrieveAPIView):
    """Api to display a  shift detail in front desk officer"""

    serializer_class = StudentListInfoSerializer
    queryset = StudentInfo.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_object(self):
        try:
            student_info = StudentInfo.objects.annotate(
                phone=F("user__phone"),
                student_first_name=F("user__first_name"),
                student_last_name=F("user__last_name"),
                faculty=F("student_academic_detail__faculty__name"),
                section=F("student_academic_detail__section__name"),
                grade=F("student_academic_detail__grade__name"),
                guardian_first_name=F("guardian_detail__user__first_name"),
                guardian_last_name=F("guardian_detail__user__last_name"),
                relation=F("guardian_detail__relation"),
                guardian_phone_number=F("guardian_detail__phone"),
                email=F("user__email"),
            ).get(id=self.kwargs.get("pk"), institution=self.request.institution)
            return student_info
        except StudentInfo.DoesNotExist:
            raise ValidationError({"error": ["Student object doesn't exist!"]})
