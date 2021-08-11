from rest_framework.permissions import BasePermission
from common.constant import SystemRole


class TeacherPermission(BasePermission):
    """
    permission to check if authenticated user is Teacher or not
    """

    def has_permission(self, request, view):
        if SystemRole.TEACHER in request.groups and request.password_updated:
            return True
        return False

