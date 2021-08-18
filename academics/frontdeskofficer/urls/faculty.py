from rest_framework.urls import path
from academics.frontdeskofficer.viewsets.faculty import (
    FacultyListAPIView,
    FacultyRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/faculty/", FacultyListAPIView.as_view()),
    path("frontdesk/faculty/<pk>/", FacultyRetrieveAPIView.as_view()),
]
