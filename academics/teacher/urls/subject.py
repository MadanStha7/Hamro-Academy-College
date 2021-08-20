from django.urls import path

from academics.teacher.viewsets.subject import TeacherSubjectView

urlpatterns = [path("teacher/subjects/", TeacherSubjectView.as_view())]
