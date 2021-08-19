from django.urls import path
from student.student.viewsets.regular_class import StudentRegularClassView

urlpatterns = [path("student_regular_class/", StudentRegularClassView.as_view())]
