from django.db.models import F
from rest_framework import status
from rest_framework.response import Response

from common.utils import active_academic_session
from onlineclass.models import OnlineClassInfo
from onlineclass.administrator.serializers.online_class import OnlineClassSerializer
from common.administrator.viewset import CommonInfoViewSet
from django_filters import rest_framework as filters
from onlineclass.administrator.custom.filter import OnlineClassFilter


class OnlineClassViewSet(CommonInfoViewSet):
    serializer_class = OnlineClassSerializer
    queryset = OnlineClassInfo.objects.none()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = OnlineClassFilter

    def get_queryset(self):
        queryset = OnlineClassInfo.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            faculty_name=F("faculty__name"),
            grade_name=F("grade__name"),
            section_name=F("section__name"),
            subject_name=F("subject__name"),
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
        print(active_session)
        serializer.save(
            created_by=self.request.user,
            institution=self.request.institution,
            academic_session=active_session,
        )
