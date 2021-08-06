from django.urls import path, include
from rest_framework import routers
from timetable.administrator.viewsets.timetable import TeacherListView, TimeTableViewSet

router = routers.DefaultRouter()
router.register("time-table", TimeTableViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("teacher-list/", TeacherListView.as_view()),
]
