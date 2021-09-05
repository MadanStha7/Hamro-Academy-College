from django.urls import path
from academics.student.views.subject import StudentSubjectView

urlpatterns = [path("subject/", StudentSubjectView.as_view())]
