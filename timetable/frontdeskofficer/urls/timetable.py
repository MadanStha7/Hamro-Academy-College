from rest_framework.urls import path
from timetable.frontdeskofficer.viewsets.timetable import (
    TimeTableListAPIView,
)

urlpatterns = [
    path("frontdesk/timetable/", TimeTableListAPIView.as_view()),
    # path("frontdesk/grade/<pk>/", GradeRetrieveAPIView.as_view()),
]
