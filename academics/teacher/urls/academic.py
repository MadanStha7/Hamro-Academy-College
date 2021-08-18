from rest_framework.urls import path

from academics.teacher.viewsets.academic import GradeAPIView, FacultyAPIView, ShiftAPIView

urlpatterns = [
    path("teacher/grades/", GradeAPIView.as_view()),
    path("teacher/faculty/", FacultyAPIView.as_view()),
    path("teacher/shift/", ShiftAPIView.as_view()),

]