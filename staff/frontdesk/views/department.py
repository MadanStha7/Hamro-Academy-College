from rest_framework import viewsets
from staff.models import Department
from staff.frontdesk.serializers.department import DepartmentListSerializer
from common.administrator.viewset import CommonInfoViewSet
from rest_framework.response import Response
from rest_framework import filters
from permissions.front_desk_officer import FrontDeskPermission
from rest_framework.permissions import IsAuthenticated
from project.custom.pagination import CustomPageSizePagination


class DepartmentView(viewsets.ViewSet):
    """
    Views for listing or retrieving inqury for administrator.
    """

    serializer_class = DepartmentListSerializer
    queryset = Department.objects.none()
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "faculty__name"]
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def list(self, request):
        """api to get list of department in front desk filtering days"""

        queryset = Department.objects.filter(institution=self.request.institution)
        queryset = self.filter_queryset(queryset)
        paginator = CustomPageSizePagination()
        result_page = paginator.paginate_queryset(queryset, self.request)
        serializer = DepartmentListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Department.objects.get(pk=pk, institution=self.request.institution)
        serializer = DepartmentListSerializer(queryset)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
