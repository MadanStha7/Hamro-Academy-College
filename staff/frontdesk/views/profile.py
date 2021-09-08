from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from staff.frontdesk.serializers.profile import ProfileSerializer
from permissions.front_desk_officer import FrontDeskPermission
from staff.models import Staff, StaffAcademicInfo


class FrontDeskProfileView(RetrieveUpdateAPIView):
    """
    API to view frontdesk profile
    """

    permission_classes = (IsAuthenticated, FrontDeskPermission)
    serializer_class = ProfileSerializer
    queryset = Staff.objects.none()

    def get_object(self):
        try:
            print("request user", self.request.user)
            staff = Staff.objects.get(user__id=self.request.user.id)
            return staff
        except Staff.DoesNotExist:
            raise PermissionDenied(
                {"unauthorized": ["you don't have enough permission"]}
            )
