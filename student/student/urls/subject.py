from django.urls import path
from student.student.viewsets.subject import StudentSubjectView

urlpatterns = [path("subject/", StudentSubjectView.as_view())]
