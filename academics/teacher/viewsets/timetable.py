from django.db.models import F
from rest_framework.generics import ListAPIView
from academics.administrator.custom_filter import TimeTableFilter
from academics.teacher.serializers.timetable import TeacherTimeTableSerializer
from timetable.models import TimeTable
from django_filters import rest_framework as filters
from collections import defaultdict
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from permissions.teacher import TeacherPermission


class TeacherTimeTableAPIView(ListAPIView):
    """Api to display a timetable list in teacher"""

    queryset = TimeTable.objects.none()
    serializer_class = TeacherTimeTableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["faculty", "grade", "shift", "section"]
    permission_classes = (IsAuthenticated, TeacherPermission)

    def list(self, request):
        """api to get list of timetable"""
        queryset = TimeTable.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            subject__name=F("subject__name"),
            teacher__firstname=F("teacher__first_name"),
            teacher__lastname=F("teacher__last_name"),
        ).order_by("start_time")
        queryset = self.filter_queryset(queryset)
        serializer = TeacherTimeTableSerializer(queryset, many=True)
        timetables = defaultdict(list)
        for data in serializer.data:
            timetables[data["day_name"]].append(data)
        return Response(timetables)
