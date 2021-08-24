from django.urls import path, include

from academics.teacher.viewsets.academic import (
    GradeAPIView,
    FacultyAPIView,
    ShiftAPIView,
)

teacher_urlpatterns = [
    path("grades/", GradeAPIView.as_view()),
    path("faculty/", FacultyAPIView.as_view()),
    path("shift/", ShiftAPIView.as_view()),
]

urlpatterns = [path("teacher/", include(teacher_urlpatterns))]
