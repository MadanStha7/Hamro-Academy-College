from django.db.models import F
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from common.administrator.viewset import CommonInfoViewSet
from common.utils import active_academic_session
from student.administator.custom_fiter import StudentAcademicFilter
from student.administator.serializer.academic import StudentAcademicSerializer,StudentAcademicDetailSerializer
from student.models import StudentAcademicDetail, StudentInfo


class StudentAcademicViewSet(CommonInfoViewSet):
    """
    CRUD for student academic.
    """

    queryset = StudentAcademicDetail.objects.none()
    serializer_class = StudentAcademicSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = StudentAcademicFilter

    def get_queryset(self):
        queryset = StudentAcademicDetail.objects.filter(
            institution=self.request.institution
        ).annotate(
            section_name=F("section__name"),
            grade_name=F("grade__name"),
            faculty_name=F("faculty__name")
        )
        return queryset

    def perform_create(self, serializer):
        student = self.request.query_params.get("student")
        if student:
            serializer.validated_data.get("previous_academic").update({
                "created_by": self.request.user, "institution": self.request.institution,
                "student": StudentInfo(id=student)})
            serializer.validated_data.get("student_academic").update({
                "created_by": self.request.user, "institution": self.request.institution,
                "academic_session": active_academic_session(self.request.institution),
                "student": StudentInfo(id=student)})
            serializer.save()
        else:
            raise ValidationError(
                {
                    "message": ["Student id is required in query param"]
                }
            )

    def create(self, request, *args, **kwargs):
        serializer = StudentAcademicDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "student academic is  successfully created"
            }
        )


