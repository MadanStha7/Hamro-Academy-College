from django.db.models import F
from rest_framework.response import Response
from common.administrator.viewset import CommonInfoViewSet
from common.utils import active_academic_session
from student.administator.serializer.academic import StudentAcademicSerializer, StudentAcademicDetailsSerializer
from student.models import StudentAcademicDetail


class StudentAcademicViewSet(CommonInfoViewSet):
    """
    CRUD for student academic.
    """

    queryset = StudentAcademicDetail.objects.none()
    serializer_class = StudentAcademicSerializer

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
        serializer.validated_data.get("previous_academic").update({
            "created_by":self.request.user, "institution": self.request.institution})
        serializer.validated_data.get("student_academic").update({
            "created_by":self.request.user, "institution": self.request.institution,
            "academic_session":active_academic_session(self.request.institution)})
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = StudentAcademicDetailsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "student academic is  successfully created"
            }
        )


