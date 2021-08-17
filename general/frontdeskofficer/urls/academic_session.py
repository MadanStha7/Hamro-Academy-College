from rest_framework.urls import path
from general.frontdeskofficer.viewsets.academic_session import (
    AcademicSessionListAPIView,
    AcademicSessionRetrieveAPIView,
)

urlpatterns = [
    path("front-desk-officer/academic-session/", AcademicSessionListAPIView.as_view()),
    path(
        "front-desk-officer/academic-session/<pk>/",
        AcademicSessionRetrieveAPIView.as_view(),
    ),
]
