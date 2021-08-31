from django.urls import path
from timetable.student.views.grade_timetable import StudentGradeTimetableView

urlpatterns = [path("grade_timetable/", StudentGradeTimetableView.as_view())]
