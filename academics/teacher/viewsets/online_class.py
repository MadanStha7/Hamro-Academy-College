from django.db.models import F
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from academics.administrator.custom_filter import OnlineClassFilter
from academics.helpers import get_online_class_values, online_class_helper

from academics.teacher.serializers.online_class import OnlineClassInfoSerializer
from common.administrator.viewset import CommonInfoViewSet
from common.utils import active_academic_session
from onlineclass.models import OnlineClassInfo
from permissions.teacher import TeacherPermission


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
        online_class = get_online_class_values(queryset)
        return online_class

    def create(self, request, *args, **kwargs):
        class_date = self.request.data.get("class_date")
        start_time = self.request.data.get("start_time")
        end_time = self.request.data.get("end_time")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = dict(serializer.data)
        online_class_helper(data, class_date, start_time, end_time)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        active_session = active_academic_session(self.request.institution)
        serializer.save(
            created_by=self.request.user,
            institution=self.request.institution,
            academic_session=active_session,
        )
