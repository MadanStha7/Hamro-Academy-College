from student.models import StudentAcademicDetail
from rest_framework.serializers import ValidationError


def student_active_academic_info(user):
    student_academic = StudentAcademicDetail.objects.filter(
        academic_session__status=True, student__user=user
    ).first()
    if student_academic:
        return student_academic
    raise ValidationError(
        {"error": "looks like you are not enrolled in any active session"}
    )
