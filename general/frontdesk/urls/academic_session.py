from rest_framework.urls import path
from general.frontdesk.views.academic_session import (
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
