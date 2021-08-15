from django.urls import path
from academics.teacher.viewsets.profile import TeacherProfileView

urlpatterns = [path("profile/<pk>/", TeacherProfileView.as_view())]
