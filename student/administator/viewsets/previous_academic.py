from django_filters import rest_framework as filters

from common.administrator.viewset import CommonInfoViewSet
from student.administator.custom_fiter import PreviousAcademicFilter
from student.administator.serializer.previous_academic import PreviousAcademicSerializer

from student.models import PreviousAcademicDetail


class PreviousAcademicViewSet(CommonInfoViewSet):
    """
    CRUD for previous academic of student.
    """

    queryset = PreviousAcademicDetail.objects.none()
    serializer_class = PreviousAcademicSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PreviousAcademicFilter

    def get_queryset(self):
        queryset = PreviousAcademicDetail.objects.filter(
            institution=self.request.institution
        )
        return queryset
