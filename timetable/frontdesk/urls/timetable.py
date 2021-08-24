from rest_framework.urls import path
from timetable.frontdesk.views.timetable import (
    TimeTableListAPIView,
)

urlpatterns = [
    path("frontdesk/timetable/", TimeTableListAPIView.as_view()),
    # path("frontdesk/grade/<pk>/", GradeRetrieveAPIView.as_view()),
]
