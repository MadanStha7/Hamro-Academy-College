from django.urls import path, include

from academics.teacher.views.timetable import TeacherTimeTableAPIView

teacher_urlpatterns = [path("timetable/", TeacherTimeTableAPIView.as_view())]

urlpatterns = [path("teacher/", include(teacher_urlpatterns))]
