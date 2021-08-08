from django.db.models import F

from common.administrator.viewset import CommonInfoViewSet
from student.administator.serializer.academic import StudentAcademicSerializer
from student.administator.serializer.previous_academic import PreviousAcademicSerializer

from student.models import StudentAcademicDetail, PreviousAcademicDetail


class PreviousAcademicViewSet(CommonInfoViewSet):
    """
    CRUD for student academic.
    """

    queryset = PreviousAcademicDetail.objects.none()
    serializer_class = PreviousAcademicSerializer

    def get_queryset(self):
        queryset = PreviousAcademicDetail.objects.filter(
            institution=self.request.institution
        )
        return queryset
