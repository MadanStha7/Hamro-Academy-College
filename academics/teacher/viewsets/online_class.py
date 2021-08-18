from django.db.models import F
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from academics.administrator.custom_filter import OnlineClassFilter

from academics.helpers import get_student_list_online_attendance
from academics.teacher.serializers.online_class import OnlineClassInfoSerializer, \
    TeacherStudentOnlineClassAttendanceSerializer

from common.administrator.viewset import CommonInfoViewSet
from common.utils import active_academic_session
from onlineclass.models import OnlineClassInfo, StudentOnlineClassAttendance
from permissions.teacher import TeacherPermission
from project.custom.pagination import CustomPageSizePagination
from student.helpers import get_online_class_attendance


class OnlineClassInfoViewSet(CommonInfoViewSet):
    """
    CRUD for online class information
    """

    serializer_class = OnlineClassInfoSerializer
    queryset = OnlineClassInfo.objects.none()
    permission_classes = (IsAuthenticated, TeacherPermission)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = OnlineClassFilter

    def get_queryset(self):
        queryset = OnlineClassInfo.objects.filter(
            institution=self.request.institution, created_by=self.request.user
        ).annotate(grade_name=F("grade__name"),
                   section_name=F("section__name"),
                   faculty_name=F("faculty__name"),
                   subject_name=F("subject__name"),
                   teacher_first_name=F('created_by__first_name'),
                   teacher_last_name=F('created_by__last_name'),
                   )
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = dict(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        active_session = active_academic_session(self.request.institution)
        serializer.save(
            created_by=self.request.user,
            institution=self.request.institution,
            academic_session=active_session,
        )


class TeacherStudentOnlineClassAttendanceView(ListAPIView):
    """
    teacher viewset, where teacher can view all the student online attendance.
    """

    permission_classes = (IsAuthenticated, TeacherPermission)
    serializer_class = TeacherStudentOnlineClassAttendanceSerializer
    queryset = StudentOnlineClassAttendance.objects.none()
    filter_fields = ["student_academic"]
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        online_class_attendance = get_online_class_attendance(self)
        return online_class_attendance

    def list(self, request, *args, **kwargs):
        online_class = self.request.query_params.get("online_class")
        online_class_info = get_object_or_404(
            OnlineClassInfo, id=online_class, created_by=self.request.user
        )
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            student_academics = get_student_list_online_attendance(
                online_class_info, self.request.general_info
            )
            data = serializer.data + list(student_academics)
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

