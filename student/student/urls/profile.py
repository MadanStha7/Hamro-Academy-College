from django.urls import path
from student.student.viewsets.profile import StudentProfileAPIView

urlpatterns = [path("student_profile/", StudentProfileAPIView.as_view())]
