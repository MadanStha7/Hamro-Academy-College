from rest_framework.urls import path
from student.frontdesk.views.student import (
    StudentListAPIView,
    StudentRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/student/", StudentListAPIView.as_view()),
    path("frontdesk/student/<pk>/", StudentRetrieveAPIView.as_view()),
]
