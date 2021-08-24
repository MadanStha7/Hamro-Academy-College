from rest_framework.urls import path
from staff.frontdesk.views.staff import (
    StaffListAPIView,
    StaffRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/staff/", StaffListAPIView.as_view()),
    path("frontdesk/staff/<pk>/", StaffRetrieveAPIView.as_view()),
]
