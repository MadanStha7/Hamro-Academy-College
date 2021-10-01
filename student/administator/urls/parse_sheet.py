from django.urls import path

from student.administator.parse_sheet import ParseStudentSheetView

urlpatterns = [
    path("parse-sheet/student/", ParseStudentSheetView.as_view(), name="parse-stusent-sheet"),
]
