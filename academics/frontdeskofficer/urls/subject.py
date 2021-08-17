from rest_framework.urls import path
from academics.frontdeskofficer.viewsets.subject import (
    SubjectListAPIView,
    SubjectRetrieveAPIView,
)

urlpatterns = [
    path("front-desk-officer/subject/", SubjectListAPIView.as_view()),
    path("front-desk-officer/subject/<pk>/", SubjectRetrieveAPIView.as_view()),
]
