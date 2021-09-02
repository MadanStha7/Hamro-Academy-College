from django.urls import path, include
from rest_framework import routers

from academics.teacher.views.academic import FacultyAPIView, ShiftAPIView, SectionAPIView, ClassAPIView

router = routers.DefaultRouter()

teacher_urlpatterns = [path("", include(router.urls)),
                       path("class/", ClassAPIView.as_view()),
                       path("section/", SectionAPIView.as_view()),
                       path("faculty/", FacultyAPIView.as_view()),
                       path("shift/", ShiftAPIView.as_view()),
                       ]
urlpatterns = [path("teacher/", include(teacher_urlpatterns))]
