from django.urls import path
from student.student.viewsets.grade import StudentGradeView

urlpatterns = [path("student_grade_timetable/", StudentGradeView.as_view())]
