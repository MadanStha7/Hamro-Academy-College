from django.urls import path
from student.student.viewsets.profile import StudentProfileAPIView

urlpatterns = [path("profile/", StudentProfileAPIView.as_view())]
