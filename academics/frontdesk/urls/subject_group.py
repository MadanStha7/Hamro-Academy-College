from rest_framework.urls import path
from academics.frontdesk.views.subject_group import (
    SubjectGroupListAPIView,
    SubjectGroupRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/subjectgroup/", SubjectGroupListAPIView.as_view()),
    path("frontdesk/subjectgroup/<pk>/", SubjectGroupRetrieveAPIView.as_view()),
]
