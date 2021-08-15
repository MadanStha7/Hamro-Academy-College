from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from academics.teacher.serializers.profile import ProfileSerializer
from permissions.teacher import TeacherPermission
from staff.models import Staff, StaffAcademicInfo


class TeacherProfileView(RetrieveUpdateAPIView):
    """
    api view of the teacher profile
    """

    permission_classes = (IsAuthenticated, TeacherPermission)
    serializer_class = ProfileSerializer
    queryset = Staff.objects.none()

    def get_object(self):
        try:
            staff = Staff.objects.get(user=self.kwargs.get("pk"))
            staff.academic_info = StaffAcademicInfo.objects.get(staff=staff)
            if staff.user == self.request.user:
                return staff
        except Staff.DoesNotExist:
            raise PermissionDenied({"unauthorized": "you don't have enough permission"})


