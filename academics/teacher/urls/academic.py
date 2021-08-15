from rest_framework.urls import path

from academics.teacher.viewsets.academic import GradeAPIView, FacultyAPIView, ShiftAPIView

urlpatterns = [
    path("my/grades/", GradeAPIView.as_view()),
    path("my/faculty/", FacultyAPIView.as_view()),
    path("my/shift/", ShiftAPIView.as_view()),

]