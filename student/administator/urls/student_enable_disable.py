from rest_framework.urls import path
from student.administator.viewsets.student_enable_disable import (
    StudentDisableAPIView,
    StudentDisableDeleteAPIView,
)

urlpatterns = [
    path("student-disable/", StudentDisableAPIView.as_view()),
    path("student-disable/delete", StudentDisableDeleteAPIView.as_view()),
]
