from django.urls import path
from student.student.viewsets.teacher import StudentTeacherView

urlpatterns = [path("student_teacher/", StudentTeacherView.as_view())]
