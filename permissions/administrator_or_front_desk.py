from rest_framework.permissions import BasePermission
from common.models import SystemRole


class AdministratorOrFrontDeskOPermission(BasePermission):
    """
    permission to check if authenticated user is Teacher or not
    """

    def has_permission(self, request, view):
        if (SystemRole.FRONT_DESK_OFFICER in request.roles) or (SystemRole.ADMINISTRATOR in request.roles):
            return True
        return False
