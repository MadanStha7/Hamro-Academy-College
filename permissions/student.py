from rest_framework.permissions import BasePermission
from common.models import SystemRole


class StudentPermission(BasePermission):
    """
    permission to check if authenticated user is Student or not
    """

    def has_permission(self, request, view):
        if SystemRole.STUDENT in request.roles:
            return True
        return False
