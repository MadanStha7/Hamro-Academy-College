from django.urls import path
from academics.teacher.viewsets.profile import TeacherProfileView

urlpatterns = [path("teacher/profile/<pk>/", TeacherProfileView.as_view())]
