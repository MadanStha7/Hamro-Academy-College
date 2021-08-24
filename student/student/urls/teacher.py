from django.urls import path
from student.student.viewsets.teacher import StudentTeacherView

urlpatterns = [path("teacher/", StudentTeacherView.as_view())]
