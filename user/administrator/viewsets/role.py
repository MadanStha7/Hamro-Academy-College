from rest_framework import viewsets
from user.models import Role
from user.administrator.serializers.role import RoleSerializer
from common.administrator.viewset import CommonInfoViewSet
from rest_framework.response import Response


class RoleViewSet(viewsets.ModelViewSet):
    """
    CRUD for role of the college.
    """

    serializer_class = RoleSerializer
    queryset = Role.objects.none()

    def get_queryset(self):
        queryset = Role.objects.filter(institution=self.request.institution)
        return queryset

    def perform_create(self, serializer):
        serializer.save(institution=self.request.institution)
