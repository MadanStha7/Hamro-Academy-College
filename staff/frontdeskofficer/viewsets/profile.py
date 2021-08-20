from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from staff.frontdeskofficer.serializers.profile import ProfileSerializer
from permissions.front_desk_officer import FrontDeskOfficerPermission
from staff.models import Staff, StaffAcademicInfo


class FrontDeskOfficerProfileView(RetrieveUpdateAPIView):
    """
    API to view frontdeskofficer profile
    """

    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)
    serializer_class = ProfileSerializer
    queryset = Staff.objects.none()

    def get_object(self):
        try:
            staff = Staff.objects.get(user=self.kwargs.get("pk"))
            if staff.user == self.request.user:
                staff.academic_info = StaffAcademicInfo.objects.get(staff=staff)
                print("logged in user", self.request.user.id)
                return staff
        except Staff.DoesNotExist:
            raise PermissionDenied(
                {"unauthorized": ["you don't have enough permission"]}
            )
