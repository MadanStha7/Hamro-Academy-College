from django.db.models import F
from rest_framework.generics import ListAPIView
from academics.teacher.serializers.timetable import TeacherTimeTableSerializer
from collections import defaultdict
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from permissions.teacher import TeacherPermission
from timetable.models import TimeTable


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
            subject_name=F("subject__name"),
            teacher_firstname=F("teacher__first_name"),
            teacher_lastname=F("teacher__last_name"),
        ).order_by("start_time")
        queryset = self.filter_queryset(queryset)
        serializer = TeacherTimeTableSerializer(queryset, many=True)
        timetables = defaultdict(list)
        for data in serializer.data:
            timetables[data["day_name"]].append(data)
        return Response(timetables)
