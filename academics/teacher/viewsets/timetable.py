from django.db.models import F
from rest_framework.generics import ListAPIView
from academics.administrator.custom_filter import TimeTableFilter
from academics.teacher.serializers.timetable import TeacherTimeTableSerializer
from timetable.models import TimeTable
from django_filters import rest_framework as filters


class TeacherTimeTableAPIView(ListAPIView):
    """
    api view where teacher can view the timetable
    """

    serializer_class = TeacherTimeTableSerializer
    queryset = TimeTable.objects.none()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TimeTableFilter

    def get_queryset(self):
        queryset = (
            TimeTable.objects.filter(
                teacher=self.request.user,
                academic_session__status=True,
            )
            .annotate(
                section_name=F("section__name"),
                grade_name=F("grade__name"),
                subject_name=F("subject__name"),
                shift_name=F("shift__name"),
                faculty_name=F("faculty__name"),
            )
            .order_by("start_time")
        )
        return queryset
