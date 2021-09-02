
from rest_framework.generics import  ListAPIView
from rest_framework.permissions import IsAuthenticated

from academics.teacher.serializers.online_class import TeacherStudentOnlineClassAttendanceSerializer

from onlineclass.models import StudentOnlineClassAttendance
from permissions.teacher import TeacherPermission
from student.helpers import get_online_class_attendance


class TeacherStudentOnlineClassAttendanceView(ListAPIView):
    """
    teacher viewset, where teacher can view all the student online attendance.
    """

    permission_classes = (IsAuthenticated, TeacherPermission)
    serializer_class = TeacherStudentOnlineClassAttendanceSerializer
    queryset = StudentOnlineClassAttendance.objects.none()

    def get_queryset(self):
        online_class_attendance = get_online_class_attendance(self)
        return online_class_attendance

