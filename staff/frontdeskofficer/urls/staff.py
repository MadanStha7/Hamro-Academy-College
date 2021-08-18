from rest_framework.urls import path
from staff.frontdeskofficer.viewsets.staff import (
    StaffListAPIView,
    StaffRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/staff/", StaffListAPIView.as_view()),
    path("frontdesk/staff/<pk>/", StaffRetrieveAPIView.as_view()),
]
