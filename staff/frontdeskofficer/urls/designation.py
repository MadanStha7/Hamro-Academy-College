from rest_framework.urls import path
from staff.frontdeskofficer.viewsets.designation import (
    DesignationListAPIView,
    DesignationRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/desgination/", DesignationListAPIView.as_view()),
    path("frontdesk/desgination/<pk>/", DesignationRetrieveAPIView.as_view()),
]
