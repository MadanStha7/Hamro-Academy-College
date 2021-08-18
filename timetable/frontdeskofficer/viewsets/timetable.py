from academics.models import Faculty, Grade, Shift, Section, Subject
from timetable.administrator.serializers.timetable import (
    TimeTableSerializer,
    TimetableListSerialzer,
    TimeTableMultipleCreateSerializer,
)

from timetable.models import TimeTable
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import F
from rest_framework import filters
from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework.generics import ListAPIView, RetrieveAPIView
from guardian.frontdeskofficer.serializer.guardianinfo import GuardianInfoSerializer
from permissions.front_desk_officer import FrontDeskOfficerPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from collections import defaultdict
from rest_framework.serializers import ValidationError


class TimeTableListAPIView(ListAPIView):
    """Api to display a timetable list in front desk officer"""

    queryset = TimeTable.objects.none()
    serializer_class = TimeTableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["faculty", "grade", "shift", "section"]
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def list(self, request):
        """api to get list of timetable"""
        queryset = TimeTable.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            subject__name=F("subject__name"),
            teacher__firstname=F("teacher__first_name"),
            teacher__lastname=F("teacher__last_name"),
        ).order_by("start_time")
        queryset = self.filter_queryset(queryset)
        serializer = TimetableListSerialzer(queryset, many=True)
        timetables = defaultdict(list)
        for data in serializer.data:
            timetables[data["day_name"]].append(data)
        return Response(timetables)
