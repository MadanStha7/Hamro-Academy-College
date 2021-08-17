from rest_framework.urls import path
from academics.frontdeskofficer.viewsets.subject_group import (
    SubjectGroupListAPIView,
    SubjectGroupRetrieveAPIView,
)

urlpatterns = [
    path("front-desk-officer/subjectgroup/", SubjectGroupListAPIView.as_view()),
    path(
        "front-desk-officer/subjectgroup/<pk>/", SubjectGroupRetrieveAPIView.as_view()
    ),
]
