from django.urls import path
from student.student.viewsets.subject import StudentSubjectView

urlpatterns = [path("student_subject/", StudentSubjectView.as_view())]
