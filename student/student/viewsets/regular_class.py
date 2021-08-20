from django.db.models import F, Value
from django.db.models.functions import Concat
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from student.student.utils.student_active_academic import student_active_academic_info
from permissions.student import StudentPermission
from student.student.serializers.regular_class import StudentRegularClassSerializer
from onlineclass.models import OnlineClassInfo


class StudentRegularClassView(ListAPIView):
    """
    student viewset, where student can view his teachers
    """

    permission_classes = (IsAuthenticated, StudentPermission)
    serializer_class = StudentRegularClassSerializer
    queryset = OnlineClassInfo.objects.none()

    def get_queryset(self):
        student_academic_id = student_active_academic_info(self.request.user)
        queryset = OnlineClassInfo.objects.filter(
            grade=student_academic_id.grade,
            faculty=student_academic_id.faculty,
            is_regular=True,
        )
        # queryset = queryset.annotate(
        #     teacher_full_name=Concat(
        #         F("teacher__first_name"),
        #         Value(' '),
        #         F("teacher__last_name"),
        #     ))
        return queryset
