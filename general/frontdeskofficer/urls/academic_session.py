from rest_framework.urls import path
from general.frontdeskofficer.viewsets.academic_session import (
    AcademicSessionListAPIView,
    AcademicSessionRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/academic-session/", AcademicSessionListAPIView.as_view()),
    path(
        "frontdesk/academic-session/<pk>/",
        AcademicSessionRetrieveAPIView.as_view(),
    ),
]
