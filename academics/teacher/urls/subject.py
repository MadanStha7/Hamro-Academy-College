from django.urls import path

from academics.teacher.viewsets.subject import TeacherSubjectView

urlpatterns = [path("my/subjects/", TeacherSubjectView.as_view())]
