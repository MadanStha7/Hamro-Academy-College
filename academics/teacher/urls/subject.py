from django.urls import path, include

from academics.teacher.views.subject import TeacherSubjectView
from academics.teacher.views.subject_group import SubjectGroupView

teacher_urlpatterns = [path("subjects/", TeacherSubjectView.as_view()),
                       path("subject_group/", SubjectGroupView.as_view()),]

urlpatterns = [path("teacher/", include(teacher_urlpatterns))]
