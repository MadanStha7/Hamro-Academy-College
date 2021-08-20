from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from permissions.student import StudentPermission
from student.administator.serializer.student import StudentInfoSerializer
from student.models import StudentInfo


class StudentProfileAPIView(RetrieveAPIView):
    """
    student profile detail api view
    """

    serializer_class = StudentInfoSerializer
    permission_classes = (IsAuthenticated, StudentPermission)

    def get_object(self):
        obj = get_object_or_404(
            StudentInfo,
            user=self.request.user,
        )
        return obj
