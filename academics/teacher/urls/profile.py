from django.urls import path, include
from academics.teacher.views.profile import TeacherProfileView

teacher_urlpatterns = [path("profile/", TeacherProfileView.as_view())]


urlpatterns = [path("teacher/", include(teacher_urlpatterns))]
