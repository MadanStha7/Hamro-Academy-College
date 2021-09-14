from rest_framework.permissions import BasePermission
from common.models import SystemRole


class AdministratorOrTeacherOrFrontDeskOPermission(BasePermission):
    """
    permission to check if authenticated user is Teacher ,administrator or frontdesk
    """

    def has_permission(self, request, view):
        if (
            (SystemRole.FRONT_DESK_OFFICER in request.roles)
            or (SystemRole.ADMINISTRATOR in request.roles)
            or (SystemRole.TEACHER in request.roles)
        ):
            return True
        return False
