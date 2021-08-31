from django.urls import path, include

from academics.teacher.views.subject import TeacherSubjectView

teacher_urlpatterns = [path("subjects/", TeacherSubjectView.as_view())]

urlpatterns = [path("teacher/", include(teacher_urlpatterns))]
