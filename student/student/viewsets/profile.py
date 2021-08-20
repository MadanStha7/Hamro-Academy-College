from django.db.models import F
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from permissions.student import StudentPermission
from student.student.serializers.profile import StudentInfoSerializer
from student.models import StudentInfo


class StudentProfileAPIView(RetrieveUpdateAPIView):
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
