from django.db.models import F
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from onlineclass.models import StudentOnlineClassAttendance, OnlineClassInfo


def get_online_class_attendance(self):
    online_class = self.request.query_params.get("online_class")
    get_object_or_404(OnlineClassInfo, id=online_class)
    if online_class:
        queryset = StudentOnlineClassAttendance.objects.filter(
            online_class=online_class,
            institution=self.request.institution,
        )
        queryset = queryset.annotate(
            online_class_title=F("online_class__title"),
            grade_name=F("online_class__grade__name"),
            section_name=F("online_class__section__name"),
            faculty_name=F("online_class__faculty__name"),
            subject_name=F("online_class__subject__name"),
            student_first_name=F("student_academic__student__user__first_name"),
            student_last_name=F("student_academic__student__user__last_name"),
        )
        return queryset
    else:
        raise ValidationError(
            [
                {"online_class": ["online_class is required query param"]},
            ]
        )
