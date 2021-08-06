from common.administrator.viewset import CommonInfoViewSet
from student.administator.serializer.category import StudentCategorySerializer
from student.models import StudentCategory


class StudentCategoryViewSet(CommonInfoViewSet):
    """
    CRUD for student category
    """

    queryset = StudentCategory.objects.none()
    serializer_class = StudentCategorySerializer

    def get_queryset(self):
        queryset = StudentCategory.objects.filter(
            institution=self.request.institution
        )
        return queryset
