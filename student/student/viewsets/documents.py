from django.db.models import F
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from permissions.student import StudentPermission
from student.student.serializers.documents import StudentDocumentSerializer
from student.models import StudentDocument, StudentInfo


class StudentDocumentAPIView(RetrieveUpdateAPIView):
    """
    student profile detail api view
    """

    serializer_class = StudentDocumentSerializer
    permission_classes = (IsAuthenticated, StudentPermission)

    def get_object(self):
        student = StudentInfo.objects.get(user=self.request.user)
        obj = get_object_or_404(StudentDocument, student=student)
        return obj
