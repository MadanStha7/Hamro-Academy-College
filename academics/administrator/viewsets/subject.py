from academics.administrator.serializers.subject import SubjectSerializer
from academics.models import Subject
from common.administrator.viewset import CommonInfoViewSet


class SubjectViewSet(CommonInfoViewSet):
    """
    CRUD for Subject lists.
    """

    queryset = Subject.objects.none()
    serializer_class = SubjectSerializer

    def get_queryset(self):
        queryset = Subject.objects.filter(institution=self.request.institution)
        return queryset
