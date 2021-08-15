from django.db.models import  F
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from academics.teacher.serializers.academic import GradeSerializer, FacultySerializer, ShiftSerializer
from permissions.teacher import TeacherPermission
from timetable.models import TimeTable


class GradeAPIView(ListAPIView):
    """
    api view of teacher for viewing the grade where he has been assigned
    """

    serializer_class = GradeSerializer
    permission_classes = (IsAuthenticated, TeacherPermission)
    queryset = TimeTable.objects.none()

    def get_queryset(self):
        queryset = TimeTable.objects.filter(teacher=self.request.user,
                                            institution=self.request.institution).order_by(
            "start_time"
        ).annotate(grade_name=F("grade__name"))
        return queryset


class FacultyAPIView(ListAPIView):
    """
    api view of teacher for viewing the faculty where he has been assigned
    """

    serializer_class = FacultySerializer
    permission_classes = (IsAuthenticated, TeacherPermission)
    queryset = TimeTable.objects.none()

    def get_queryset(self):
        queryset = TimeTable.objects.filter(teacher=self.request.user,
                                            institution=self.request.institution).annotate(
            faculty_name=F("faculty__name"))
        return queryset


class ShiftAPIView(ListAPIView):
    """
    api view of teacher for viewing the faculty where he has been assigned
    """

    serializer_class = ShiftSerializer
    permission_classes = (IsAuthenticated, TeacherPermission)
    queryset = TimeTable.objects.none()

    def get_queryset(self):
        queryset = TimeTable.objects.filter(teacher=self.request.user,
                                            institution=self.request.institution).annotate(
            shift_name=F("shift__name"))
        return queryset





