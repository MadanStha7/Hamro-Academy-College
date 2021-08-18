from rest_framework.urls import path
from academics.frontdeskofficer.viewsets.faculty import (
    FacultyListAPIView,
    FacultyRetrieveAPIView,
)

urlpatterns = [
    path("front-desk-officer/faculty/", FacultyListAPIView.as_view()),
    path("front-desk-officer/faculty/<pk>/", FacultyRetrieveAPIView.as_view()),
]
