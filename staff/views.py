from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from rest_framework.response import Response

from permissions.administrator import AdministratorPermission
from student.administator.serializer.student import StudentInfoSerializer
from student.models import StudentInfo


class GetStudentInfoBulkView(APIView):
    """API View to list of student of provided ids"""

    permission_classes = (IsAuthenticated, AdministratorPermission)

    def post(self, request, *args, **kwargs):
        student = self.request.data.get("student")
        if student and isinstance(student, list):
            staffs = StudentInfo.objects.filter(
                id__in=student, institution=self.request.institution
            ).annotate(
                student_first_name=F("user__first_name"),
                student_middle_name=F("user__middle_name"),
                student_last_name=F("user__last_name"))
            serializer = StudentInfoSerializer(staffs, many=True)
            return Response(serializer.data)
        raise ValidationError({"student": ["expected list of student id"]})
