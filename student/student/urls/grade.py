from django.urls import path
from student.student.viewsets.grade import StudentGradeView

urlpatterns = [path("grade_timetable/", StudentGradeView.as_view())]
