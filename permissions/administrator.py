from rest_framework.permissions import BasePermission
from common.constant import SystemRole


class AdministratorPermission(BasePermission):
    """
    permission to check if authenticated user is Teacher or not
    """

    def has_permission(self, request, view):
        if SystemRole.ADMINISTRATOR in request.roles:
            return True
        return False
