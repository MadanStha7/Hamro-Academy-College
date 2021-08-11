from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
User = get_user_model()


class TeacherPermission(BasePermission):
    """
    permission to check if authenticated user is Teacher or not
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.roles.filter(title="Teacher"):
            print("teacher")
            return True
        return False

