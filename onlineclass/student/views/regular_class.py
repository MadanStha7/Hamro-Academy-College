from django.db.models import F, Value
from django.db.models.functions import Concat
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from student.student.utils.student_active_academic import student_active_academic_info
from permissions.student import StudentPermission
from onlineclass.student.serializers.regular_class import StudentRegularClassSerializer
from onlineclass.models import OnlineClassInfo
from django_filters import rest_framework as filters
from onlineclass.administrator.custom.filter import OnlineClassFilter


class StudentRegularClassView(ListAPIView):
    """
    student viewset, where student can view his regular online class
    """

    permission_classes = (IsAuthenticated, StudentPermission)
    serializer_class = StudentRegularClassSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = OnlineClassFilter

    def get_queryset(self):
        student_academic_id = student_active_academic_info(self.request.user)
        queryset = OnlineClassInfo.objects.filter(
            grade=student_academic_id.grade,
            faculty=student_academic_id.faculty,
            is_regular=True,
        )
        queryset = queryset.annotate(
            faculty_name=F("faculty__name"),
            grade_name=F("grade__name"),
            section_name=F("section__name"),
            subject_name=F("subject__name"),
        )

        return queryset
