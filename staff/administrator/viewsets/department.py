from rest_framework import viewsets
from staff.models import Department
from staff.administrator.serializers.department import DepartmentSerializer
from common.administrator.viewset import CommonInfoViewSet
from rest_framework.response import Response
from rest_framework import filters


class DepartmentViewset(CommonInfoViewSet):
    """
    CRUD for department of the staff.
    """

    serializer_class = DepartmentSerializer
    queryset = Department.objects.none()
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "faculty__name"]

    def get_queryset(self):
        queryset = Department.objects.filter(institution=self.request.institution)
        return queryset
