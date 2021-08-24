from rest_framework.urls import path
from staff.frontdesk.views.designation import (
    DesignationListAPIView,
    DesignationRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/desgination/", DesignationListAPIView.as_view()),
    path("frontdesk/desgination/<pk>/", DesignationRetrieveAPIView.as_view()),
]
