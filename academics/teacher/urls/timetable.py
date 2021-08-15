from django.urls import path

from academics.teacher.viewsets.timetable import TeacherTimeTableAPIView

urlpatterns = [path("timetable/", TeacherTimeTableAPIView.as_view())]
