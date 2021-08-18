from rest_framework.urls import path
from academics.frontdeskofficer.viewsets.grade import (
    GradeListAPIView,
    GradeRetrieveAPIView,
)

urlpatterns = [
    path("front-desk-officer/grade/", GradeListAPIView.as_view()),
    path("front-desk-officer/grade/<pk>/", GradeRetrieveAPIView.as_view()),
]
