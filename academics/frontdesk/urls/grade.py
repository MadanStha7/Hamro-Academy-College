from rest_framework.urls import path
from academics.frontdesk.views.grade import (
    GradeListAPIView,
    GradeRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/grade/", GradeListAPIView.as_view()),
    path("frontdesk/grade/<pk>/", GradeRetrieveAPIView.as_view()),
]
