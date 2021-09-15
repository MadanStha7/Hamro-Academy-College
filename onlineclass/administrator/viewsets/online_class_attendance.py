from permissions.administrator_or_teacher_or_frontdesk import (
    AdministratorOrTeacherOrFrontDeskOPermission,
)
from rest_framework.permissions import IsAuthenticated
from student.models import StudentAcademicDetail
from django.db.models import F, Value
from django.db.models.functions import Concat
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from onlineclass.administrator.custom.filter import OnlineClassAttendanceFilter
from onlineclass.models import OnlineClassInfo, StudentOnlineClassAttendance
from onlineclass.administrator.serializers.online_class_attendance import (
    StudentOnlineClassAttendanceSerializer,
    StudentAcademicSerializer,
)
from common.administrator.viewset import CommonInfoViewSet
from rest_framework.response import Response


class StudentOnlineClassAttendanceViewSet(CommonInfoViewSet):
    serializer_class = StudentOnlineClassAttendanceSerializer
    queryset = StudentOnlineClassAttendance.objects.none()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = OnlineClassAttendanceFilter
    permission_classes = [IsAuthenticated, AdministratorOrTeacherOrFrontDeskOPermission]

    def get_queryset(self):
        queryset = StudentOnlineClassAttendance.objects.filter(
            institution=self.request.institution
        )
        queryset = queryset.annotate(
            onlineclass_title=F("online_class__title"),
            student_full_name=Concat(
                F("student_academic__student__user__first_name"),
                Value(" "),
                F("student_academic__student__user__last_name"),
            ),
        )

        return queryset

    @action(detail=True, methods=["get"])
    def log(self, request, pk=None):
        online_class_id = self.kwargs.get("pk")
        online_class = OnlineClassInfo.objects.get(id=online_class_id)
        grade = online_class.grade
        faculty = online_class.faculty
        student_academic_detail = StudentAcademicDetail.objects.filter(
            grade=grade, faculty=faculty, institution=self.request.institution
        )
        return Response(
            StudentAcademicSerializer(
                student_academic_detail,
                many=True,
                context={
                    "online_class": online_class.id,
                    "institution": self.request.institution,
                },
            ).data
        )
